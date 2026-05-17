import asyncio, json, os, requests
from .soul_initializer import get_soul

HUB_URL = "http://127.0.0.1:3002"
KEYS = [os.environ.get(k) for k in ["OPENROUTER_KEY_FREE_1","OPENROUTER_KEY_FREE_2","OPENROUTER_KEY_FREE_4","OPENROUTER_KEY_FREE_5","OPENROUTER_API_KEY"] if os.environ.get(k)]
DEFAULT_MODEL = "deepseek/deepseek-v4-flash:free"

class BaseAgent:
    def __init__(self, name, desc, trigger, sys_prompt=None, poll=5, model=None):
        self.n, self.d, self.t, self.sys, self.p, self.model = name, desc, trigger, sys_prompt, poll, model or DEFAULT_MODEL
        self.seen, self._ki = set(), 0
        soul = get_soul(name)
        if not self.sys:
            from .tool_registry import format_tools_prompt
            self.sys = format_tools_prompt(soul, name)
            if "role" in soul: self.sys += f"\nRolle: {soul['role']}"

    def post(self, path, json=None):
        try: return requests.post(f"{HUB_URL}{path}", json=json).json()
        except: return {}

    def put(self, path, params=None):
        try: return requests.put(f"{HUB_URL}{path}", params=params).json()
        except: return {}

    def get(self, path):
        try: return requests.get(f"{HUB_URL}{path}").json()
        except: return []

    def _llm(self, msgs):
        for i in range(len(KEYS)):
            k = KEYS[(self._ki + i) % len(KEYS)]
            try:
                r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {k}"}, json={"model": self.model, "messages": msgs}, timeout=30).json()
                if "choices" in r: self._ki = (self._ki + i) % len(KEYS); return r["choices"][0]["message"]["content"]
            except: pass
        return None

    async def run(self):
        self.post("/api/agents/register", {"name": self.n, "port": 0, "description": self.d})
        print(f"🚀 {self.n} aktiv (model={self.model}, keys={len(KEYS)})")
        while True:
            chat = self.get("/api/chat?limit=10")
            if not isinstance(chat, list): chat = []
            new = [m for m in chat if m.get("id") not in self.seen and (self.n.lower() in m.get("content", "").lower() or "@all" in m.get("content", "").lower())]
            for m in chat: self.seen.add(m.get("id"))
            for m in new:
                reply = self._llm([{"role": "system", "content": self.sys}, {"role": "user", "content": m["content"]}])
                if reply: self.post("/api/chat", {"content": reply, "sender": self.n})
                else: print(f"[{self.n}] Alle Keys fehlgeschlagen")
            await asyncio.sleep(self.p)
