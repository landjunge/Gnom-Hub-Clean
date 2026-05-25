# monitoring.py — Agent Health Monitoring & Heartbeat Tracker
import time

METRICS = {}

def record_agent_request(agent: str, duration_ms: float, success: bool):
    name = agent.lower()
    if name not in METRICS:
        METRICS[name] = {"total": 0, "failed": 0, "avg_time_ms": 0.0, "last_seen": 0.0}
    m = METRICS[name]
    m["total"] += 1
    if not success:
        m["failed"] += 1
    m["last_seen"] = time.time()
    m["avg_time_ms"] = ((m["avg_time_ms"] * (m["total"] - 1)) + duration_ms) / m["total"]

def get_agent_metrics() -> dict:
    now = time.time()
    return {
        name: {
            **m,
            "success_rate": (m["total"] - m["failed"]) / m["total"] if m["total"] > 0 else 1.0,
            "status": "online" if now - m["last_seen"] < 120 else "offline"
        }
        for name, m in METRICS.items()
    }
