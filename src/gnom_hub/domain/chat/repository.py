from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from .entities import ChatMessage, FlexSoul


class ChatRepository(ABC):
    """Abstraktes Repository-Interface für Chat-Verläufe und FlexSoul."""

    @abstractmethod
    async def get_messages(self, agent_id: UUID, limit: int = 50) -> List[ChatMessage]:
        """Lädt die letzten Nachrichten eines Agenten."""
        pass

    @abstractmethod
    async def save_message(self, message: ChatMessage) -> ChatMessage:
        """Speichert eine neue Nachricht."""
        pass

    @abstractmethod
    async def get_flexsoul(self, agent_id: UUID) -> Optional[FlexSoul]:
        """Lädt das FlexSoul-Gedächtnis eines Agenten."""
        pass

    @abstractmethod
    async def save_flexsoul(self, flexsoul: FlexSoul) -> FlexSoul:
        """Speichert das FlexSoul-Gedächtnis."""
        pass

    @abstractmethod
    async def clear_history(self, agent_id: UUID) -> bool:
        """Löscht den gesamten Chat-Verlauf eines Agenten."""
        pass
