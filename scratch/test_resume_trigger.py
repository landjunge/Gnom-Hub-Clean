import httpx

url = "http://127.0.0.1:3002/api/chat"
payload = {
    "sender": "user",
    "content": "@@resume CoderAG"
}

print("Sende Resume...")
r = httpx.post(url, json=payload)
print("Response status:", r.status_code)
print("Response JSON:", r.json())
