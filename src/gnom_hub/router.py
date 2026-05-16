import os, json, requests
from dotenv import load_dotenv

load_dotenv()

# Priorisierte Liste unserer kostenlosen Keys (Das Magazin)
KEYS = [
    ("Nvidia-Neutron", os.getenv("OPENROUTER_KEY_NVIDIA_NEUTRON"), "nvidia/nemotron-4-340b-instruct:free"),
    ("Free-1", os.getenv("OPENROUTER_KEY_FREE_1"), "google/gemma-2-9b-it:free"),
    ("Free-2", os.getenv("OPENROUTER_KEY_FREE_2"), "meta-llama/llama-3-8b-instruct:free"),
    ("Fallback-DeepSeek", os.getenv("DEEPSEEK_API_KEY"), "deepseek-chat") # Letzte Rettung
]

def ask_router(prompt, sys_prompt="Du bist ein hilfreicher Assistent."):
    """Feuert auf den ersten Key. Fällt er aus, wird sofort der nächste geladen."""
    for name, key, model in KEYS:
        if not key: continue # Überspringe leere Keys
        
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            if "deepseek" in name.lower():
                url = "https://api.deepseek.com/chat/completions"

            print(f"\n[ROUTER] Versuche Gleis: {name} ({model})...")
            
            res = requests.post(
                url,
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": model, "messages": [{"role": "system", "content": sys_prompt}, {"role": "user", "content": prompt}]}
            )
            
            if res.status_code == 200:
                print(f"[ROUTER] Erfolg auf Gleis {name}!")
                return res.json()['choices'][0]['message']['content']
            else:
                print(f"[ROUTER] Gleis {name} gescheitert (Code {res.status_code}). Schalte um...")
                
        except Exception as e:
            print(f"[ROUTER] Absturz auf Gleis {name}: {e}. Schalte um...")
            
    return "[ROUTER-FEHLER] Alle Gleise offline. Die Nebelwand ist undurchdringlich."
