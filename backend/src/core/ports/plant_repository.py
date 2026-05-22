from abc import ABC, abstractmethod
from uuid import UUID

from src.core.entities.plant import GrowthStage, Plant, PlantType


class PlantRepository(ABC):

    @abstractmethod
    async def create(
        self, user_id: UUID, plant_type: PlantType
    ) -> Plant: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Plant | None: ...

    @abstractmethod
    async def get_by_id(self, plant_id: UUID) -> Plant | None: ...

    @abstractmethod
    async def update_stage(
        self,
        plant_id: UUID,
        stage: GrowthStage,
        total_drops: int,
        drops_in_stage: int,
    ) -> None: ...

    @abstractmethod
    async def increment_drops(
        self, plant_id: UUID, amount: int
    ) -> None: ...
