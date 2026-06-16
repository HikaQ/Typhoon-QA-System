import time
import requests

MAX_RETRIES = 3
RETRY_DELAY = 1  # 秒，指数递增


class SiliconFlowLLM:
    def __init__(self, api_key, base_url, model, timeout=30):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def chat(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        last_error = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.post(
                    self.base_url,
                    json=payload,
                    timeout=self.timeout
                )

                print(f"LLM HTTP 状态码: {resp.status_code} (第{attempt}次尝试)")

                if resp.status_code == 200:
                    data = resp.json()
                    if "choices" in data:
                        return data["choices"][0]["message"]["content"]
                    return f"模型返回结构异常: {data}"

                # 5xx 服务器错误 → 重试
                if resp.status_code >= 500 and attempt < MAX_RETRIES:
                    print(f"LLM 服务器错误 {resp.status_code}，{RETRY_DELAY * attempt}s 后重试...")
                    time.sleep(RETRY_DELAY * attempt)
                    continue

                return f"大模型服务异常（HTTP {resp.status_code}）"

            except requests.exceptions.Timeout:
                last_error = "timeout"
                if attempt < MAX_RETRIES:
                    print(f"LLM 超时（第{attempt}次），{RETRY_DELAY * attempt}s 后重试...")
                    time.sleep(RETRY_DELAY * attempt)
                else:
                    return "系统繁忙，请稍后重试"

            except requests.exceptions.ConnectionError:
                last_error = "connection"
                if attempt < MAX_RETRIES:
                    print(f"LLM 连接错误（第{attempt}次），{RETRY_DELAY * attempt}s 后重试...")
                    time.sleep(RETRY_DELAY * attempt)
                else:
                    return "系统繁忙，请稍后重试"

            except Exception as e:
                return f"调用大模型异常: {str(e)}"

        return "系统繁忙，请稍后重试"

    def close(self):
        self.session.close()
