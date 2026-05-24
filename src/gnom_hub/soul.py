from .db import save_soul_fact, get_relevant_facts

class SoulAG:
    def __init__(self):
        self.name = "SoulAG"
    
    def on_message(self, message: str, sender: str):
        """Wird bei jeder Nachricht im Chat aufgerufen"""
        if sender == "user":
            self._extract_and_save(message)
    
    def _extract_and_save(self, message: str):
        """Erkennt und speichert wichtige Informationen"""
        # Hier kommt später eine LLM-basierte Extraktion hin
        keywords = ["passwort", "password", "key", "token", "api", "zugang", "secret", "benutzer"]
        if any(k in message.lower() for k in keywords):
            save_soul_fact(message)  # vorerst die ganze Nachricht speichern
    
    def inject_context(self, agent_prompt: str, user_message: str) -> str:
        """Injiziert relevante Infos unsichtbar in den System-Prompt"""
        relevant = get_relevant_facts(user_message)
        if not relevant:
            return agent_prompt
            
        injection = "\n\nRelevante Informationen aus meinem Gedächtnis:\n" + "\n".join(relevant)
        return agent_prompt + injection

soul_instance = SoulAG()
