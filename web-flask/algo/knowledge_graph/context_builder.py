def build_context(graph_data):
    if not graph_data:
        return "未检索到相关台风信息。"

    def safe(v):
        return v if v else "未知"

    # 强度级别映射（用于排序）
    LEVEL_RANK = {
        "热带低压": 0,
        "热带风暴": 1,
        "强热带风暴": 2,
        "台风": 3,
        "强台风": 4,
        "超强台风": 5,
    }

    def get_level_rank(level):
        return LEVEL_RANK.get(level, -1)

    # 同名台风多个匹配的情况
    if isinstance(graph_data, dict) and "results" in graph_data:
        # 按年份和名称合并数据
        aggregated = {}
        for t in graph_data["results"]:
            key = (t.get('name'), t.get('year'))
            if key not in aggregated:
                aggregated[key] = {
                    "name": t.get('name'),
                    "year": t.get('year'),
                    "levels": set(),
                    "provinces": set()
                }
            aggregated[key]["levels"].add(t.get('level'))
            if t.get('province'):
                aggregated[key]["provinces"].add(t.get('province'))

        # 排序并构建输出
        lines = []
        for (name, year), data in sorted(aggregated.items(), key=lambda x: x[0][1], reverse=True):
            # 获取最强强度
            levels = sorted(data["levels"], key=get_level_rank, reverse=True)
            max_level = levels[0] if levels else "未知"
            
            # 省份列表
            provinces = "、".join(sorted(data["provinces"])) if data["provinces"] else "未知"
            
            lines.append(
                f"【{safe(name)} {safe(year)}年】\n"
                f"  强度：{max_level}\n"
                f"  登陆省份：{provinces}"
            )
        
        return f"发现【{graph_data.get('typhoon')}】有多个同名台风，按年份排序：\n\n" + "\n\n".join(lines)

    # 列表
    if "typhoons" in graph_data:
        lines = [f"{t.get('name')}（{safe(t.get('level'))}）" for t in graph_data["typhoons"]]
        return f"{safe(graph_data.get('year'))} 年台风列表：" + "、".join(lines)

    # 单个
    return (
        f"台风【{safe(graph_data.get('name'))}】\n"
        f"- 年份：{safe(graph_data.get('year'))}\n"
        f"- 登陆省份：{safe(graph_data.get('province'))}\n"
        f"- 登陆时间：{safe(graph_data.get('date'))}\n"
        f"- 强度：{safe(graph_data.get('level'))}\n"
        f"- 影响：{safe(graph_data.get('impact'))}"
    )