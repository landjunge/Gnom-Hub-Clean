from fastapi import Depends
from ..infrastructure.database.agent_repo import SQLiteAgentRepository as AR
from ..infrastructure.database.chat_repo import SQLiteChatRepository as CR
from ..infrastructure.llm.orchestrator import LLMOrchestrator as LO
from ..infrastructure.process.manager import ProcessManager as PM
from ..infrastructure.admin.service import AdminService as AS
from ..application.agent.commands import AgentCommands as AC
from ..application.agent.queries import AgentQueries as AQ
from ..application.chat.service import ChatService as CS
from ..application.chat.send_message import SendMessageUseCase as SM
from ..application.chat.brainstorm import BrainstormUseCase as BS

# Singletons & Services
def get_agent_repo(): return AR()
def get_chat_repo(): return CR()
def get_process_manager(): return PM()
def get_llm_orchestrator(): return LO()
def get_admin_service(): return AS()

def get_agent_commands(repo=Depends(get_agent_repo), pm=Depends(get_process_manager)):
    return AC(repo, pm)

def get_agent_queries(repo=Depends(get_agent_repo)):
    return AQ(repo)

def get_send_message_use_case(chat_repo=Depends(get_chat_repo), agent_repo=Depends(get_agent_repo), llm=Depends(get_llm_orchestrator)):
    return SM(chat_repo, agent_repo, llm)

def get_brainstorm_use_case(repo=Depends(get_agent_repo), llm=Depends(get_llm_orchestrator)):
    return BS(repo, llm)

def get_chat_service(send_uc=Depends(get_send_message_use_case), brainstorm_uc=Depends(get_brainstorm_use_case)):
    return CS(send_uc, brainstorm_uc)
