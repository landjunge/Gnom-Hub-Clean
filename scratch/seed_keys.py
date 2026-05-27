#!/usr/bin/env python3
"""Seeds the .env API keys into the gnomhub.db and resets agents to auto routing."""
import sqlite3, json, os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(str(env_path))

db_path = os.environ.get("GNOM_HUB_HOME", str(Path.home() / ".gnom-hub"))
db_path = Path(db_path) / "data" / "gnomhub.db"
print(f"DB: {db_path}")

conn = sqlite3.connect(str(db_path))

keys = {}
idx = 0

# DeepSeek
ds_key = os.getenv("DEEPSEEK_API_KEY")
if ds_key:
    kid = f"k_env_{idx}"
    keys[kid] = {"id": kid, "key": ds_key, "provider": "deepseek", "valid": True, "info": "OK", "caps": ["text", "tools"], "label": "DEEPSEEK_API_KEY"}
    idx += 1
    print(f"  + DeepSeek key loaded")

# OpenRouter keys
for env_name in ["OPENROUTER_API_KEY", "OPENROUTER_KEY_FREE_1", "OPENROUTER_KEY_FREE_2", "OPENROUTER_KEY_FREE_3", "OPENROUTER_KEY_FREE_4", "OPENROUTER_KEY_NVIDIA_NEUTRON", "OPENROUTER_MANAGEMENT_KEY"]:
    val = os.getenv(env_name)
    if val:
        kid = f"k_env_{idx}"
        keys[kid] = {"id": kid, "key": val, "provider": "openrouter", "valid": True, "info": "OK", "caps": ["text", "vision", "tools"], "label": env_name}
        idx += 1
        print(f"  + OpenRouter key: {env_name}")

conn.execute("INSERT OR REPLACE INTO state (key, value) VALUES (?, ?)", ("llm_keys", json.dumps(keys)))

# Reset agents to auto
agents = {}
for name in ["soulag", "generalag", "watchdogag", "securityag", "coderag", "writerag", "researcherag", "editorag"]:
    agents[name] = {"provider": "auto", "model": "stage_3"}
conn.execute("INSERT OR REPLACE INTO state (key, value) VALUES (?, ?)", ("llm_agents", json.dumps(agents)))

conn.commit()
conn.close()
print(f"\n{len(keys)} Keys gespeichert, {len(agents)} Agents auf auto/stage_3 gesetzt.")
