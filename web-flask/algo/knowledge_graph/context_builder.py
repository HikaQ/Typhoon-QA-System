def build_context(graph_data):
    if not graph_data:
        return "知识图谱中未检索到相关台风记录。"

    # 年份台风列表
    if "typhoons" in graph_data:
        lines = [f"{t['name']}（{t.get('level','未知')}）" for t in graph_data["typhoons"]]
        return f"{graph_data['year']} 年台风列表：" + "、".join(lines)

    # 单台风详情
    return f"""
台风【{graph_data.get('name')}】
- 年份：{graph_data.get('year')}
- 登陆省份：{graph_data.get('province')}
- 登陆时间：{graph_data.get('date')}
- 强度：{graph_data.get('level')}
- 影响：{graph_data.get('impact')}
""".strip()
