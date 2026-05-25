import time; from .db import get_state_value, set_state_value
from gnom_hub.infrastructure.router.router_call import _call, _try_keys
from gnom_hub.structured_log import AgentLogger; from gnom_hub.monitoring import record_agent_request
def _try(pvd, mdl, key, msgs, n):
    try: return _call(pvd, mdl, key, msgs, n)
    except Exception: return None
def ask_router(p, sys="Du bist ein Assistent.", agent_name=None):
    n, t0 = (agent_name or "").lower(), time.time()
    active_preset = (get_state_value("active_preset") or "Web Development").strip('"\'')
    if n in ["coderag", "researcherag", "writerag", "editorag"]:
        from .preset_service import get_preset_prompt
        preset_prompt = get_preset_prompt(active_preset, n)
        if preset_prompt: sys = preset_prompt + "\n\n" + sys
    msgs = [{"role": "system", "content": sys}, {"role": "user", "content": p}]
    kdb, adb = get_state_value("llm_keys") or {}, get_state_value("llm_agents") or {}
    cfg = adb.get(n) or {"provider": "auto", "model": "stage_3"}
    pvd, mdl = cfg.get("provider", "auto"), cfg.get("model", "stage_3")
    if pvd == "auto":
        from gnom_hub.infrastructure.router.router_stage import SmartRouter
        r_pvd, r_mdl = SmartRouter.resolve_stage(mdl, kdb, n)
        cands = [(r_pvd, r_mdl)] if r_pvd == "lokal" else [(r_pvd, r_mdl), ("lokal", "llama3.2")]
    else: cands = [("lokal", mdl)] if pvd == "lokal" else [(pvd, mdl), ("lokal", "llama3.2")]
    logger = AgentLogger(agent_name or "Unknown")
    for cp, cm in cands:
        ans = _try("lokal", cm, "", msgs, agent_name) if cp == "lokal" else _try_keys(cp, cm, kdb, msgs, agent_name)
        if ans:
            lat = (time.time() - t0) * 1000; record_agent_request(n or "unknown", lat, True)
            logger.log_event("llm_call", provider=cp, model=cm, latency_ms=lat, status="success")
            if cfg.get("provider") != cp or cfg.get("model") != cm:
                if cfg.get("provider") != "auto":
                    adb[n] = {"provider": cp, "model": cm}; set_state_value("llm_agents", adb)
            if n:
                from .swarm_comms import process_swarm_mentions
                process_swarm_mentions(agent_name or n, ans)
            return ans
    lat = (time.time() - t0) * 1000; record_agent_request(n or "unknown", lat, False)
    logger.log_event("llm_call", latency_ms=lat, status="failed")
    return "[ROUTER-FEHLER] Alle Gleise offline."
