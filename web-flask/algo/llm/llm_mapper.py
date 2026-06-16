from .llm_client import SiliconFlowLLM
from .config_loader import config

_llm = None
_cache = {}


def _get_llm():
    global _llm
    if _llm is None:
        sf = config.get("siliconflow", {})
        _llm = SiliconFlowLLM(
            api_key=sf.get("api_key"),
            base_url=sf.get("base_url"),
            model=sf.get("model"),
            timeout=sf.get("timeout", 60)
        )
    return _llm


def map_typhoon_name(question, typhoon_list):
    if question in _cache:
        return _cache[question]

    prompt = f"""
你是一个台风名称标准化助手。

背景：
台风的中文名是从英文名音译过来的。例如：
- "杜苏芮" 对应 "Doksuri"（发音相似：du-su-rui → Dok-su-ri）
- "利奇马" 对应 "Lekima"
- "海高斯" 对应 "Higos"
- "鹦鹉" 对应 "Nuri"

任务：
根据发音相似性，从用户问题中识别台风的中文名，匹配对应的标准英文名。

【用户问题】
{question}

【候选台风英文名】
{typhoon_list[:200]}

要求：
1. 根据中文发音与英文发音的对应关系来匹配，不要随意猜测
2. 只返回一个英文台风名称
3. 如果没有匹配，返回：None
4. 不要解释，不要输出其他内容

输出：
"""

    result = _get_llm().chat(prompt).strip()

    print("LLM返回：", result)

    if "None" in result:
        _cache[question] = None
        return None

    for name in typhoon_list:
        if name.lower() in result.lower():
            _cache[question] = name
            return name

    _cache[question] = None
    return None
