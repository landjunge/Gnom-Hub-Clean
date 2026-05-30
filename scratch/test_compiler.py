# test_compiler.py — Tests compilation, prompt baking, SQLite pruning, and startup integrity
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

def setup_test_environment():
    from gnom_hub.db.schema import init_database
    init_database()

def create_test_data():
    from gnom_hub.db.legacy_db import get_db_conn
    from gnom_hub.core.utils.evolution_v2 import create_version
    import uuid
    from datetime import datetime, timezone
    
    with get_db_conn() as conn:
        with conn:
            conn.execute("DELETE FROM prompt_versions")
            conn.execute("DELETE FROM chat")
            
    create_version("CoderAG", "Evolved Rule 1: Always add tests.")
    
    now = datetime.now(timezone.utc)
    with get_db_conn() as conn:
        with conn:
            for i in range(1005):
                ts = now.isoformat()
                conn.execute(
                    "INSERT INTO chat (id, project, sender, agent_id, msg_type, content, timestamp, metadata) "
                    "VALUES (?, 'default', 'User', 'coderag', 'chat', ?, ?, '{}')",
                    (str(uuid.uuid4()), f"Message {i}", ts)
                )

def run_compilation():
    from gnom_hub.core.utils.compiler import bake_supergnom
    dist_dir = bake_supergnom("test_gnom")
    return dist_dir

def verify_baked_prompts(dist_dir):
    from pathlib import Path
    dist_path = Path(dist_dir)
    target_def_file = dist_path / "src" / "gnom_hub" / "agents" / "agent_definitions.py"
    assert target_def_file.exists(), f"{target_def_file} does not exist"
    
    loc = {}
    with open(target_def_file, "r", encoding="utf-8") as f:
        exec(f.read(), globals(), loc)
        
    agent_defs = loc["AGENT_DEFINITIONS"]
    coder_sys_prompt = agent_defs["coderag"]["sys_prompt"]
    assert "Evolved Rule 1" in coder_sys_prompt, f"Expected evolved prompt, got: {coder_sys_prompt}"

def verify_manifest_json(dist_dir):
    import json
    import hashlib
    from pathlib import Path
    dist_path = Path(dist_dir)
    manifest_path = dist_path / "config" / "manifest.json"
    assert manifest_path.exists(), f"{manifest_path} does not exist"
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    target_def_file = dist_path / "src" / "gnom_hub" / "agents" / "agent_definitions.py"
    loc = {}
    with open(target_def_file, "r", encoding="utf-8") as f:
        exec(f.read(), globals(), loc)
    agent_defs = loc["AGENT_DEFINITIONS"]
    
    for k, v in agent_defs.items():
        name = v["name"]
        expected_hash = manifest[name]
        p_bytes = v["sys_prompt"].encode("utf-8")
        current_hash = hashlib.sha256(p_bytes).hexdigest()
        assert current_hash == expected_hash, f"Hash mismatch for {name}"

def verify_database_cleanup(dist_dir):
    import sqlite3
    from pathlib import Path
    dist_path = Path(dist_dir)
    db_dest = dist_path / ".gnom-hub" / "data" / "gnomhub.db"
    assert db_dest.exists(), f"{db_dest} does not exist"
    
    conn = sqlite3.connect(str(db_dest))
    cursor = conn.cursor()
    
    cursor.execute("SELECT count(*) FROM chat")
    chat_count = cursor.fetchone()[0]
    assert chat_count == 1000, f"Expected exactly 1000 chat messages, got {chat_count}"
    
    for tbl in ["audit_log", "explainable_outputs", "graceful_degradation_failures", 
                "token_budget_logs", "token_budget_alerts"]:
        cursor.execute(f"SELECT count(*) FROM {tbl}")
        cnt = cursor.fetchone()[0]
        assert cnt == 0, f"Table {tbl} was not cleared, contains {cnt} rows"
        
    conn.close()

def verify_compiled_startup(dist_dir):
    import subprocess
    import sys
    import os
    from pathlib import Path
    
    dist_path = Path(dist_dir)
    src_dir = dist_path / "src"
    
    env = {
        **os.environ,
        "PYTHONPATH": str(src_dir),
        "SUPERGNOM_MODE": "True",
        "GNOM_HUB_HOME": str(dist_path / ".gnom-hub")
    }
    
    code = (
        "import sys, os\n"
        "from gnom_hub.core.config import CONFIG_DIR\n"
        "import json, hashlib\n"
        "from gnom_hub.agents.agent_definitions import AGENT_DEFINITIONS\n"
        "manifest_path = CONFIG_DIR / 'manifest.json'\n"
        "with open(manifest_path, 'r', encoding='utf-8') as f:\n"
        "    manifest = json.load(f)\n"
        "corrupted = []\n"
        "for name, expected_hash in manifest.items():\n"
        "    for k, v in AGENT_DEFINITIONS.items():\n"
        "        if v['name'].lower() == name.lower():\n"
        "            p_bytes = v['sys_prompt'].encode('utf-8')\n"
        "            current_hash = hashlib.sha256(p_bytes).hexdigest()\n"
        "            if current_hash != expected_hash:\n"
        "                corrupted.append(v['name'])\n"
        "if corrupted:\n"
        "    sys.exit(1)\n"
        "sys.exit(0)\n"
    )
    
    res = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
    assert res.returncode == 0, f"Integrity check failed: {res.stderr}\nSTDOUT: {res.stdout}"

def verify_compiled_startup_corrupted(dist_dir):
    import subprocess
    import sys
    import os
    from pathlib import Path
    
    dist_path = Path(dist_dir)
    src_dir = dist_path / "src"
    
    target_def_file = src_dir / "gnom_hub" / "agents" / "agent_definitions.py"
    with open(target_def_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    corrupted_content = content.replace("Evolved Rule 1", "Corrupted Rule 1")
    with open(target_def_file, "w", encoding="utf-8") as f:
        f.write(corrupted_content)
        
    env = {
        **os.environ,
        "PYTHONPATH": str(src_dir),
        "SUPERGNOM_MODE": "True",
        "GNOM_HUB_HOME": str(dist_path / ".gnom-hub")
    }
    
    code = (
        "import sys, os\n"
        "from gnom_hub.core.config import CONFIG_DIR\n"
        "import json, hashlib\n"
        "from gnom_hub.agents.agent_definitions import AGENT_DEFINITIONS\n"
        "manifest_path = CONFIG_DIR / 'manifest.json'\n"
        "with open(manifest_path, 'r', encoding='utf-8') as f:\n"
        "    manifest = json.load(f)\n"
        "corrupted = []\n"
        "for name, expected_hash in manifest.items():\n"
        "    for k, v in AGENT_DEFINITIONS.items():\n"
        "        if v['name'].lower() == name.lower():\n"
        "            p_bytes = v['sys_prompt'].encode('utf-8')\n"
        "            current_hash = hashlib.sha256(p_bytes).hexdigest()\n"
        "            if current_hash != expected_hash:\n"
        "                corrupted.append(v['name'])\n"
        "if corrupted and 'CoderAG' in corrupted:\n"
        "    sys.exit(0)\n"
        "sys.exit(1)\n"
    )
    
    res = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
    assert res.returncode == 0, f"Corruption detection failed: {res.stderr}\nSTDOUT: {res.stdout}"

def verify_app_lifespan(dist_dir):
    import subprocess
    import sys
    import os
    from pathlib import Path
    
    dist_path = Path(dist_dir)
    src_dir = dist_path / "src"
    
    env = {
        **os.environ,
        "PYTHONPATH": str(src_dir),
        "SUPERGNOM_MODE": "True",
        "GNOM_HUB_HOME": str(dist_path / ".gnom-hub")
    }
    
    code = (
        "import asyncio, os\n"
        "import gnom_hub.api.app as app_mod\n"
        "app_mod.start_background_agents = lambda: None\n"
        "async def mock_updater():\n"
        "    while True:\n"
        "        await asyncio.sleep(3600)\n"
        "app_mod.start_openrouter_updater = mock_updater\n"
        "async def run_test():\n"
        "    async with app_mod.lifespan(None):\n"
        "        print('LIFESPAN_STARTED')\n"
        "asyncio.run(run_test())\n"
    )
    res = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
    assert "LIFESPAN_STARTED" in res.stdout, f"Lifespan startup failed: {res.stderr}\nSTDOUT: {res.stdout}"

def cleanup_test_artifacts(dist_dir):
    import shutil
    from pathlib import Path
    path = Path(dist_dir)
    if path.exists():
        shutil.rmtree(path)

def test_compiler():
    print("--- STARTING SUPERGNOM COMPILER INTEGRATION TEST ---")
    setup_test_environment()
    create_test_data()
    
    dist_dir = run_compilation()
    print(f"Compilation finished. Dist dir: {dist_dir}")
    
    try:
        verify_baked_prompts(dist_dir)
        verify_manifest_json(dist_dir)
        verify_database_cleanup(dist_dir)
        verify_compiled_startup(dist_dir)
        verify_app_lifespan(dist_dir)
        verify_compiled_startup_corrupted(dist_dir)
        print("✅ SuperGNOM compilation tests passed successfully!")
    finally:
        cleanup_test_artifacts(dist_dir)

if __name__ == "__main__":
    test_compiler()
