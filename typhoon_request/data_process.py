"""
台风数据预处理脚本
从 IBTrACS 原始数据中筛选中国区域台风（2000-2026），生成用于 Neo4j 导入的 CSV 文件。

数据来源：
    IBTrACS (International Best Track Archive for Climate Stewardship)
    下载地址：https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/
    文件名：ibtracs.WP.list.v04r01.csv（西北太平洋区域）

使用方法：
    python data_process.py

输出文件：
    - china_typhoon_list_2000_2026.csv  — 台风列表
    - china_typhoon_path_2000_2026.csv  — 路径点数据
    - sample_typhoon.csv                — 演示用小样本（前50个台风）
"""
import pandas as pd

# ==================== 配置 ====================
RAW_DATA_PATH = "typhoon_request/ibtracs.WP.list.v04r01.csv"
OUTPUT_PATH_CSV = "typhoon_request/china_typhoon_path_2000_2026.csv"
OUTPUT_LIST_CSV = "typhoon_request/china_typhoon_list_2000_2026.csv"
OUTPUT_SAMPLE_CSV = "typhoon_request/sample_typhoon.csv"

YEAR_START = 2000
YEAR_END = 2026

# 中国大致经纬度范围
LAT_MIN, LAT_MAX = 15, 55
LON_MIN, LON_MAX = 100, 135

# 需要保留的字段
KEEP_COLUMNS = ["SID", "SEASON", "NAME", "ISO_TIME", "LAT", "LON", "USA_WIND", "USA_PRES"]


def main():
    # ========= 1. 读取原始数据 =========
    print("=" * 50)
    print("台风数据预处理")
    print("=" * 50)
    print(f"\n[1/5] 读取原始数据: {RAW_DATA_PATH}")
    df = pd.read_csv(RAW_DATA_PATH, low_memory=False)
    print(f"  原始数据量: {len(df)} 条")

    # ========= 2. 字段筛选 =========
    print(f"\n[2/5] 筛选字段: {KEEP_COLUMNS}")
    df = df[KEEP_COLUMNS]

    # ========= 3. 数据清洗 =========
    print("\n[3/5] 数据清洗...")
    for col in ["SEASON", "LAT", "LON", "USA_WIND", "USA_PRES"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 删除关键字段为空的行
    df = df.dropna(subset=["SEASON", "LAT", "LON", "NAME"])
    df["SEASON"] = df["SEASON"].astype(int)
    print(f"  清洗后: {len(df)} 条")

    # ========= 4. 年份 + 中国范围筛选 =========
    print(f"\n[4/5] 筛选 {YEAR_START}-{YEAR_END} 年 + 中国区域...")
    df = df[
        (df["SEASON"] >= YEAR_START) & (df["SEASON"] <= YEAR_END) &
        (df["LAT"] >= LAT_MIN) & (df["LAT"] <= LAT_MAX) &
        (df["LON"] >= LON_MIN) & (df["LON"] <= LON_MAX)
    ]
    print(f"  筛选后: {len(df)} 条路径记录")

    # ========= 5. 生成输出文件 =========
    print("\n[5/5] 生成输出文件...")

    # 路径数据
    df.to_csv(OUTPUT_PATH_CSV, index=False, encoding="utf-8-sig")
    print(f"  ✅ {OUTPUT_PATH_CSV}（{len(df)} 条）")

    # 台风列表（去重）
    typhoon_list = df[["SID", "NAME", "SEASON"]].drop_duplicates()
    typhoon_list.to_csv(OUTPUT_LIST_CSV, index=False, encoding="utf-8-sig")
    print(f"  ✅ {OUTPUT_LIST_CSV}（{len(typhoon_list)} 个台风）")

    # 演示用小样本
    sample = typhoon_list.head(50)
    sample.to_csv(OUTPUT_SAMPLE_CSV, index=False, encoding="utf-8-sig")
    print(f"  ✅ {OUTPUT_SAMPLE_CSV}（{len(sample)} 个台风，演示用）")

    print("\n" + "=" * 50)
    print("✅ 预处理完成！接下来请运行: python typhoon_import.py")
    print("=" * 50)


if __name__ == "__main__":
    main()
