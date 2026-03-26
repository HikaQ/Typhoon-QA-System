import re

PROVINCES = ["福建", "广东", "浙江", "海南", "台湾"]

def extract_entities(question: str):
    result = {
        "year": None,
        "province": None
    }

    # 抽取年份
    year = re.search(r"(20\d{2})", question)
    if year:
        result["year"] = int(year.group(1))

    # 抽取省份
    for p in PROVINCES:
        if p in question:
            result["province"] = p
            break

    return result
