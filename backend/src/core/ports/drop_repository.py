from abc import ABC, abstractmethod
from uuid import UUID

from src.core.entities.drop import Drop, DropEventType


class DropRepository(ABC):

    @abstractmethod
    async def create(
        self,
        plant_id: UUID,
        event_type: DropEventType,
        source_repo: str,
        github_event_id: str,
        committed_at: object,
    ) -> Drop: ...

    @abstractmethod
    async def exists_by_github_event_id(
        self, github_event_id: str
    ) -> bool: ...

    @abstractmethod
    async def list_by_plant_id(
        self,
        plant_id: UUID,
        limit: int = 20,
        cursor: str | None = None,
    ) -> tuple[list[Drop], str | None]: ...
