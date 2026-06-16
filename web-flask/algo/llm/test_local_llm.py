"""
本地 LLM + 联网搜索 测试脚本

流程：
  用户提问 → 联网搜索 → 搜索结果喂给本地模型 → 返回基于实时数据的回答
"""
import json
import time
import requests
from ddgs import DDGS


def search_web(query: str, max_results: int = 5) -> str:
    """联网搜索，返回格式化文本"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return "未搜索到相关结果。"
        lines = []
        for i, r in enumerate(results, 1):
            lines.append(f"[{i}] {r['title']}\n    {r['body']}\n    来源: {r['href']}")
        return "\n\n".join(lines)
    except Exception as e:
        return f"搜索失败: {e}"


class LocalOllamaLLM:
    def __init__(self, model="deepseek-r1:7b", base_url="http://localhost:11434", timeout=600):
        self.model = model
        self.base_url = base_url
        self.timeout = timeout
        self.chat_url = f"{base_url}/api/chat"
        self.session = requests.Session()
        self.session.headers["Content-Type"] = "application/json"

    def chat_with_search(self, user_question: str, search_query: str = None) -> dict:
        """先联网搜索，再让本地模型基于搜索结果回答"""
        query = search_query or user_question

        print(f"[搜索] {query}")
        search_text = search_web(query)

        prompt = f"""你是一个台风知识助手。请根据以下联网搜索结果回答用户问题。

【联网搜索结果】
{search_text}

【用户问题】
{user_question}

请基于搜索结果回答。如果搜索结果不足，请如实说明。用中文回答，简洁明了。"""

        print("[回答]", end=" ", flush=True)
        t0 = time.time()

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }
        resp = self.session.post(self.chat_url, json=payload, timeout=self.timeout, stream=True)

        full_response = []
        for line in resp.iter_lines():
            if not line:
                continue
            try:
                chunk = json.loads(line)
                if "message" in chunk and "content" in chunk["message"]:
                    token = chunk["message"]["content"]
                    print(token, end="", flush=True)
                    full_response.append(token)
            except json.JSONDecodeError:
                continue

        elapsed = time.time() - t0
        print(f"\n[耗时] {elapsed:.1f}s\n")
        return {"content": "".join(full_response), "elapsed": round(elapsed, 1)}

    def close(self):
        self.session.close()


if __name__ == "__main__":
    llm = LocalOllamaLLM()

    # --- 自定义你想问的问题 ---
    tests = [
        ("目前西太平洋有哪些活跃的台风？",    "2026年5月 西太平洋 台风 最新"),
        ("最近有没有台风要登陆中国？",        "2026年5月 台风登陆 中国"),
        ("广东最近会受台风影响吗？",          "2026年5月 广东 台风 最新消息"),
    ]

    for question, search_keyword in tests:
        print(f"\n{'=' * 60}")
        print(f"问题: {question}")
        print("=" * 60)
        llm.chat_with_search(question, search_keyword)

    llm.close()
