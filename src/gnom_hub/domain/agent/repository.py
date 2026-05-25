from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from .entities import Agent


class AgentRepository(ABC):
    """Abstraktes Repository-Interface für Agenten."""

    @abstractmethod
    async def get_by_id(self, agent_id: UUID) -> Optional[Agent]:
        """Lädt einen Agenten per ID."""
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Agent]:
        """Lädt einen Agenten per Namen."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Agent]:
        """Gibt alle Agenten zurück."""
        pass

    @abstractmethod
    async def save(self, agent: Agent) -> Agent:
        """Speichert oder aktualisiert einen Agenten."""
        pass

    @abstractmethod
    async def delete(self, agent_id: UUID) -> bool:
        """Löscht einen Agenten."""
        pass
