import re
import sys
from difflib import get_close_matches
from .neo4j_client import Neo4jClient
from .config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from algo.llm.llm_mapper import map_typhoon_name

PROVINCES = ["福建", "广东", "浙江", "海南", "台湾"]

_neo4j_client = None
_neo4j_available = None
TYPHOON_NAMES = []


def _get_client():
    global _neo4j_client, _neo4j_available
    if _neo4j_available is not None:
        return _neo4j_client
    try:
        _neo4j_client = Neo4jClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
        _neo4j_client.run("RETURN 1")
        _neo4j_available = True
    except Exception as e:
        _neo4j_client = None
        _neo4j_available = False
        print(f"[KG] Neo4j 不可用, 实体提取将降级: {e}", file=sys.stderr)
    return _neo4j_client


def _init_typhoon_names():
    global TYPHOON_NAMES
    if TYPHOON_NAMES:
        return
    client = _get_client()
    if client is None:
        return
    try:
        cypher = "MATCH (t:Typhoon) RETURN DISTINCT t.name AS name"
        result = client.run(cypher)
        TYPHOON_NAMES = [r["name"] for r in result if r["name"]]
    except Exception:
        pass


def get_all_years_for_typhoon(typhoon_name):
    client = _get_client()
    if client is None:
        return []
    cypher = "MATCH (t:Typhoon {name: $name}) RETURN DISTINCT t.year AS year ORDER BY t.year DESC"
    result = client.run(cypher, {"name": typhoon_name})
    return [r["year"] for r in result]


def extract_entities(question: str):
    _init_typhoon_names()

    result = {
        "year": None,
        "province": None,
        "typhoon": None,
        "all_matching_years": None
    }

    year = re.search(r"(20\d{2})", question)
    if year:
        result["year"] = int(year.group(1))

    for p in PROVINCES:
        if p in question:
            result["province"] = p
            break

    for name in TYPHOON_NAMES:
        if name and name in question:
            result["typhoon"] = name
            all_years = get_all_years_for_typhoon(name)
            if len(all_years) > 1:
                result["all_matching_years"] = all_years
            return result

    words = re.findall(r"[一-龥]{2,}", question)
    for w in words:
        match = get_close_matches(w, TYPHOON_NAMES, n=1, cutoff=0.7)
        if match:
            result["typhoon"] = match[0]
            all_years = get_all_years_for_typhoon(match[0])
            if len(all_years) > 1:
                result["all_matching_years"] = all_years
            return result

    llm_result = map_typhoon_name(question, TYPHOON_NAMES)
    if llm_result:
        result["typhoon"] = llm_result
        all_years = get_all_years_for_typhoon(llm_result)
        if len(all_years) > 1:
            result["all_matching_years"] = all_years

    return result
