from .neo4j_client import Neo4jClient
from .config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
import sys

_neo4j_client = None
_neo4j_available = None


def _get_client():
    global _neo4j_client, _neo4j_available
    if _neo4j_available is not None:
        return _neo4j_client
    try:
        _neo4j_client = Neo4jClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
        # 测试连接
        _neo4j_client.run("RETURN 1")
        _neo4j_available = True
        print("[KG] Neo4j 连接成功", file=sys.stderr)
    except Exception as e:
        _neo4j_client = None
        _neo4j_available = False
        print(f"[KG] Neo4j 不可用，知识图谱功能将禁用: {e}", file=sys.stderr)
    return _neo4j_client


def is_available():
    _get_client()
    return _neo4j_available


def _deduplicate_results(results):
    seen = set()
    deduped = []
    for result in results:
        key = (
            result.get("name"),
            result.get("year"),
            result.get("province"),
            result.get("level")
        )
        if key not in seen:
            seen.add(key)
            deduped.append(result)
    return deduped


def retrieve_knowledge(entities):
    client = _get_client()
    if client is None:
        return {"error": "Neo4j 不可用，知识图谱查询暂不可用"}

    year = entities.get("year")
    province = entities.get("province")
    typhoon = entities.get("typhoon")

    if typhoon:
        if year:
            cypher = """
            MATCH (t:Typhoon {name: $typhoon, year: $year})
            OPTIONAL MATCH (t)-[:LANDED_IN]->(p:Province)
            OPTIONAL MATCH (t)-[:HAS_LEVEL]->(l:Level)
            RETURN DISTINCT
                t.name AS name,
                t.year AS year,
                p.name AS province,
                l.value AS level
            """
            result = client.run(cypher, {"typhoon": typhoon, "year": year})
            result = _deduplicate_results(result)
            return result[0] if result else {}
        else:
            cypher = """
            MATCH (t:Typhoon {name: $typhoon})
            OPTIONAL MATCH (t)-[:LANDED_IN]->(p:Province)
            OPTIONAL MATCH (t)-[:HAS_LEVEL]->(l:Level)
            RETURN DISTINCT
                t.name AS name,
                t.year AS year,
                p.name AS province,
                l.value AS level
            ORDER BY t.year DESC
            """
            result = client.run(cypher, {"typhoon": typhoon})
            result = _deduplicate_results(result)
            return {
                "typhoon": typhoon,
                "multiple_matches": len(result) > 1,
                "results": result
            } if result else {}

    if year and province:
        cypher = """
        MATCH (t:Typhoon {year: $year})
        OPTIONAL MATCH (t)-[:LANDED_IN]->(p:Province {name: $province})
        OPTIONAL MATCH (t)-[:HAS_LEVEL]->(l:Level)
        WHERE p IS NOT NULL
        RETURN DISTINCT t.name AS name, l.value AS level
        """
        result = client.run(cypher, {
            "year": year,
            "province": province
        })
        result = _deduplicate_results(result)
        return {
            "year": year,
            "province": province,
            "typhoons": result
        }

    if year:
        cypher = """
        MATCH (t:Typhoon {year: $year})
        OPTIONAL MATCH (t)-[:HAS_LEVEL]->(l:Level)
        RETURN DISTINCT t.name AS name, l.value AS level
        """
        result = client.run(cypher, {"year": year})
        result = _deduplicate_results(result)
        return {
            "year": year,
            "typhoons": result
        }

    return {}
