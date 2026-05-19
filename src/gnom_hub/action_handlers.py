# action_handlers.py — Dispatcher für alle Action-Tags
import re
from .action_write import handle_write, handle_read
from .action_exec import handle_shell, handle_crawl, handle_showbox

def process_actions(answer, agent, perms, bs_mode, wd):
    """Verarbeitet alle Action-Tags in einer LLM-Antwort."""
    answer = handle_write(answer, list(re.finditer(r"\[WRITE:\s*(.*?)\](.*?)\[/WRITE\]", answer, re.DOTALL)), agent, perms, bs_mode, wd)
    answer = handle_read(answer, list(re.finditer(r"\[READ:\s*(.*?)\]", answer)), wd)
    answer = handle_shell(answer, list(re.finditer(r"\[SHELL:\s*(.*?)\]", answer)), agent, perms, bs_mode, wd)
    answer = handle_crawl(answer, list(re.finditer(r"\[CRAWL:\s*(.*?)\]", answer)), agent, perms)
    answer = handle_showbox(answer, list(re.finditer(r"\[SHOWBOX:\s*(.*?)\]", answer, re.DOTALL)))
    return answer
