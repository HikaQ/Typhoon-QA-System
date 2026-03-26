from .neo4j_client import Neo4jClient
from .config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

neo4j_client = Neo4jClient(
    NEO4J_URI,
    NEO4J_USER,
    NEO4J_PASSWORD
)

def retrieve_knowledge(entities):
    year = entities.get("year")
    province = entities.get("province")
    typhoon = entities.get("typhoon")

    # 台风详情查询
    if typhoon:
        cypher = """
        MATCH (t:Typhoon {name: $typhoon})-[:OCCURRED_IN]->(y:Year)
        OPTIONAL MATCH (t)-[:LANDED_IN]->(p:Province)
        OPTIONAL MATCH (t)-[:HAS_LEVEL]->(l:Level)
        OPTIONAL MATCH (t)-[:HAS_DATE]->(d:Date)
        OPTIONAL MATCH (t)-[:HAS_IMPACT]->(i:Impact)
        RETURN 
            t.name AS name,
            y.value AS year,
            p.name AS province,
            l.value AS level,
            d.value AS date,
            i.value AS impact
        """
        result = neo4j_client.run(cypher, {"typhoon": typhoon})
        return result[0] if result else {}

    # 年份 + 省份
    if year and province:
        cypher = """
        MATCH (t:Typhoon)-[:OCCURRED_IN]->(y:Year {value: $year})
        MATCH (t)-[:LANDED_IN]->(p:Province {name: $province})
        OPTIONAL MATCH (t)-[:HAS_LEVEL]->(l:Level)
        RETURN t.name AS name, l.value AS level
        """
        result = neo4j_client.run(cypher, {
            "year": year,
            "province": province
        })
        return {
            "year": year,
            "province": province,
            "typhoons": result
        }

    # 仅按年份查询
    if year:
        cypher = """
        MATCH (t:Typhoon)-[:OCCURRED_IN]->(y:Year {value: $year})
        OPTIONAL MATCH (t)-[:HAS_LEVEL]->(l:Level)
        RETURN t.name AS name, l.value AS level
        """
        result = neo4j_client.run(cypher, {"year": year})
        return {
            "year": year,
            "typhoons": result
        }

    return {}
