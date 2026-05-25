from fastapi import APIRouter, Request; import requests, os, platform, psutil
router = APIRouter()
@router.get("/api/llm/available_models")
def get_available_models():
    ds_models = ["deepseek-chat", "deepseek-reasoner"]
    or_models = []
    try:
        r = requests.get("https://openrouter.ai/api/v1/models", timeout=5)
        if r.status_code == 200: or_models = [m["id"] for m in r.json().get("data", []) if m.get("id", "").endswith(":free")]
    except Exception: pass
    if not or_models: or_models = ['deepseek/deepseek-v4-flash:free', 'qwen/qwen3-coder:free', 'meta-llama/llama-3.3-70b-instruct:free']
    local_models = []
    try:
        r = requests.get("http://127.0.0.1:11434/api/tags", timeout=3)
        if r.status_code == 200: local_models = [m["name"] for m in r.json().get("models", []) if m.get("name")]
    except Exception: pass
    if not local_models: local_models = ['llama3', 'mistral', 'qwen2', 'phi3', 'llama3.2', 'gemma2']
    return {
        "auto": ["stage_1", "stage_2", "stage_3", "stage_4"],
        "deepseek": ds_models, "openrouter": or_models, "lokal": local_models
    }
@router.get("/api/system/info")
def get_system_info():
    cpu = platform.processor() or platform.machine()
    try:
        import subprocess
        cpu = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception: pass
    ram = f"{round(psutil.virtual_memory().total / (1024**3))} GB"
    return {"cpu": cpu, "ram": ram, "is_intel": "intel" in cpu.lower()}
@router.post("/api/restart")
def restart_server(request: Request):
    from agents.securityAG import _get_or_create_secret
    if request.headers.get("X-Hub-Secret") != _get_or_create_secret().hex(): return {"error": "Unauthorized"}
    import sys, subprocess; subprocess.Popen([sys.executable] + sys.argv); os._exit(0)
