import os
from .router_config import DS_KEY, OR_KEY

def get_keys(pvd, kdb):
    ks = [k.get("key") for k in (kdb.values() if isinstance(kdb, dict) else kdb) if k.get("provider") == pvd and k.get("valid")]
    if pvd == "deepseek" and DS_KEY: ks.append(DS_KEY)
    elif pvd == "openrouter":
        ks.extend([os.environ.get(f"OPENROUTER_KEY_FREE_{i}") for i in range(1, 6) if os.environ.get(f"OPENROUTER_KEY_FREE_{i}")])
        if OR_KEY: ks.append(OR_KEY)
    return list(dict.fromkeys(ks))
