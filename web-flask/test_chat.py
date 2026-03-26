import requests

url = "http://127.0.0.1:5000/chat/ask"
data = {"question": "北京有台风吗？"}

r = requests.post(url, json=data)
print(r.json())
