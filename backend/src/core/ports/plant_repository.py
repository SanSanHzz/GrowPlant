from abc import ABC, abstractmethod
from uuid import UUID

from src.core.entities.plant import Plant, PlantType, GrowthStage


class PlantRepository(ABC):

    @abstractmethod
    async def create(
        self, user_id: UUID, plant_type: PlantType, is_active: bool = False
    ) -> Plant: ...

    @abstractmethod
    async def list_by_user_id(self, user_id: UUID) -> list[Plant]: ...

    @abstractmethod
    async def get_active(self, user_id: UUID) -> Plant | None: ...

    @abstractmethod
    async def get_by_id(self, plant_id: UUID) -> Plant | None: ...

    @abstractmethod
    async def set_active(self, plant_id: UUID, user_id: UUID) -> None: ...

    @abstractmethod
    async def update_stage(
        self,
        plant_id: UUID,
        stage: GrowthStage,
        total_drops: int,
        drops_in_stage: int,
    ) -> None: ...

    @abstractmethod
    async def update_name(
        self, plant_id: UUID, name: str
    ) -> None: ...

    @abstractmethod
    async def delete(self, plant_id: UUID) -> None: ...

    @abstractmethod
    async def increment_drops(
        self, plant_id: UUID, amount: int
    ) -> None: ...
