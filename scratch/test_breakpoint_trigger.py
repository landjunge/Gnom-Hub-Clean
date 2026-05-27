import httpx
import time

url = "http://127.0.0.1:3002/api/chat"
payload = {
    "sender": "user",
    "content": "@CoderAG schreibe eine Datei namens 'test_breakpoint.txt' mit dem Inhalt 'Breakpoint-Test'"
}

print("Sende Nachricht...")
r = httpx.post(url, json=payload)
print("Response status:", r.status_code)
print("Response JSON:", r.json())
