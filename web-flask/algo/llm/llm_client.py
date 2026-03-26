import requests

class SiliconFlowLLM:
    def __init__(self, api_key, base_url, model, timeout=30):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        try:
            resp = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )

            print("LLM HTTP 状态码:", resp.status_code)
            print("LLM 原始返回:", resp.text)

            if resp.status_code != 200:
                return f"大模型服务异常（HTTP {resp.status_code}）"

            data = resp.json()

            # 硅基流动是 OpenAI 风格
            if "choices" not in data:
                return f"模型返回结构异常: {data}"

            return data["choices"][0]["message"]["content"]

        except Exception as e:
            return f"调用大模型异常: {str(e)}"
