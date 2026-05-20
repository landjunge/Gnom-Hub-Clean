class DynamicSouls(dict):
    def _active_dict(self):
        from .db import get_language
        from . import soul_initializer_de, soul_initializer_en
        return soul_initializer_en.SOULS if get_language() == "en" else soul_initializer_de.SOULS

    def items(self): return self._active_dict().items()
    def keys(self): return self._active_dict().keys()
    def values(self): return self._active_dict().values()
    def get(self, k, d=None): return self._active_dict().get(k, d)
    def __getitem__(self, k): return self._active_dict()[k]
    def __iter__(self): return iter(self._active_dict())
    def __len__(self): return len(self._active_dict())
    def __contains__(self, k): return k in self._active_dict()

SOULS = DynamicSouls()

def get_soul(agent_name: str) -> dict:
    from .db import get_language
    lang = get_language()
    default_directive = "Help the swarm." if lang == "en" else "Hilf dem Schwarm."
    return SOULS.get(agent_name.lower(), {"role": "default", "permissions": ["read"], "directive": default_directive})
