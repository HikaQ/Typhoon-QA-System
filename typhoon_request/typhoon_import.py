"""
台风知识图谱数据导入脚本
将处理好的台风 CSV 数据导入 Neo4j 图数据库

使用方法：
    python typhoon_import.py

前提条件：
    1. Neo4j 数据库已启动
    2. 已运行 data_process.py 生成 china_typhoon_*.csv
    3. 修改下方的连接配置
"""
from neo4j import GraphDatabase
import pandas as pd

# ==================== 连接配置（按需修改） ====================
URI = "neo4j://localhost:7687"
USER = "neo4j"
PASSWORD = "12345678"

# ==================== 数据文件路径 ====================
TYPHOON_LIST_CSV = "typhoon_request/china_typhoon_list_2000_2026.csv"
TYPHOON_PATH_CSV = "typhoon_request/china_typhoon_path_2000_2026.csv"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


# ==================== 工具函数 ====================

def get_province(lat, lon):
    """根据经纬度判断所属省份（简化版）"""
    if 20 <= lat <= 28 and 109 <= lon <= 118:
        return "广东"
    elif 23 <= lat <= 31 and 116 <= lon <= 123:
        return "福建"
    elif 27 <= lat <= 35 and 118 <= lon <= 123:
        return "浙江"
    elif 18 <= lat <= 22 and 108 <= lon <= 112:
        return "海南"
    return None


def get_level(wind):
    """根据风速（节）返回台风等级"""
    if wind is None or pd.isna(wind):
        return "未知"
    if wind >= 51:
        return "超强台风"
    elif wind >= 41:
        return "强台风"
    elif wind >= 33:
        return "台风"
    elif wind >= 17:
        return "热带风暴"
    else:
        return "热带低压"


# ==================== 数据库写入 ====================

def import_typhoon_node(tx, row):
    """创建台风节点"""
    tx.run("""
        MERGE (t:Typhoon {sid: $sid})
        SET t.name = $name,
            t.season = $season
    """, {
        "sid": row["SID"],
        "name": row["NAME"],
        "season": int(row["SEASON"])
    })


def import_path_point(tx, row):
    """创建路径点及相关知识图谱节点"""
    lat = float(row["LAT"])
    lon = float(row["LON"])
    wind = float(row["USA_WIND"]) if pd.notna(row["USA_WIND"]) else None
    pressure = float(row["USA_PRES"]) if pd.notna(row["USA_PRES"]) else None
    level = get_level(wind)
    province = get_province(lat, lon)
    iso_time = row["ISO_TIME"]
    year = int(row["SEASON"])
    # 提取日期部分（前10位为日期）
    date = str(iso_time)[:10]

    # 创建路径点及其关联节点
    tx.run("""
        MATCH (t:Typhoon {sid: $sid})

        MERGE (y:Year {value: $year})
        MERGE (t)-[:OCCURRED_IN]->(y)

        MERGE (l:Level {value: $level})
        MERGE (t)-[:HAS_LEVEL]->(l)

        MERGE (d:Date {value: $date})
        MERGE (t)-[:HAS_DATE]->(d)

        CREATE (p:PathPoint {
            lat: $lat,
            lon: $lon,
            wind: $wind,
            pressure: $pressure,
            time: $time
        })
        MERGE (t)-[:HAS_PATH]->(p)
    """, {
        "sid": row["SID"],
        "year": year,
        "level": level,
        "date": date,
        "lat": lat,
        "lon": lon,
        "wind": wind,
        "pressure": pressure,
        "time": iso_time
    })

    # 如果识别到省份，创建登录关系
    if province:
        tx.run("""
            MATCH (t:Typhoon {sid: $sid})
            MERGE (p:Province {name: $province})
            MERGE (t)-[:LANDED_IN]->(p)
        """, {
            "sid": row["SID"],
            "province": province
        })


# ==================== 主程序 ====================

def main():
    print("=" * 50)
    print("台风知识图谱数据导入")
    print("=" * 50)

    # 第一步：导入台风列表
    print("\n[1/2] 导入台风节点...")
    typhoon_df = pd.read_csv(TYPHOON_LIST_CSV)
    print(f"  读取到 {len(typhoon_df)} 个台风")

    with driver.session() as session:
        for i, (_, row) in enumerate(typhoon_df.iterrows()):
            session.execute_write(import_typhoon_node, row)
            if (i + 1) % 100 == 0:
                print(f"  已导入 {i + 1}/{len(typhoon_df)} 个台风...")
    print(f"  ✅ 台风节点导入完成（共 {len(typhoon_df)} 个）")

    # 第二步：导入路径点及关联图谱
    print("\n[2/2] 导入路径点及知识图谱...")
    path_df = pd.read_csv(TYPHOON_PATH_CSV)
    print(f"  读取到 {len(path_df)} 条路径记录")

    with driver.session() as session:
        for i, (_, row) in enumerate(path_df.iterrows()):
            session.execute_write(import_path_point, row)
            if (i + 1) % 1000 == 0:
                print(f"  已导入 {i + 1}/{len(path_df)} 条路径...")
    print(f"  ✅ 路径数据导入完成（共 {len(path_df)} 条）")

    print("\n" + "=" * 50)
    print("✅ 全部导入完成！")
    print("=" * 50)
    print("\n图谱节点类型：")
    print("  - Typhoon（台风）     — 台风基本信息")
    print("  - PathPoint（路径点） — 台风轨迹点（风、气压、经纬度）")
    print("  - Year（年份）        — 发生年份")
    print("  - Level（等级）       — 台风强度等级")
    print("  - Date（日期）        — 发生日期")
    print("  - Province（省份）    — 登录省份")
    print("\n图谱关系类型：")
    print("  - HAS_PATH      — 台风 → 路径点")
    print("  - OCCURRED_IN   — 台风 → 年份")
    print("  - HAS_LEVEL     — 台风 → 等级")
    print("  - HAS_DATE      — 台风 → 日期")
    print("  - LANDED_IN     — 台风 → 登录省份")


if __name__ == "__main__":
    main()
