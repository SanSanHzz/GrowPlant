from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entities.plant import GrowthStage, Plant, PlantType
from src.core.ports.plant_repository import PlantRepository
from src.infrastructure.database.models.plant import PlantModel


class PostgresPlantRepository(PlantRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_entity(model: PlantModel) -> Plant:
        return Plant(
            id=model.id,
            user_id=model.user_id,
            plant_type=PlantType(model.plant_type),
            current_stage=GrowthStage(model.current_stage),
            total_drops=model.total_drops,
            drops_in_stage=model.drops_in_stage,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def create(
        self, user_id: UUID, plant_type: PlantType
    ) -> Plant:
        model = PlantModel(
            user_id=user_id,
            plant_type=plant_type.value,
            current_stage=1,
            total_drops=0,
            drops_in_stage=0,
        )
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_user_id(self, user_id: UUID) -> Plant | None:
        stmt = select(PlantModel).where(PlantModel.user_id == user_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_id(self, plant_id: UUID) -> Plant | None:
        stmt = select(PlantModel).where(PlantModel.id == plant_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def update_stage(
        self,
        plant_id: UUID,
        stage: GrowthStage,
        total_drops: int,
        drops_in_stage: int,
    ) -> None:
        stmt = (
            update(PlantModel)
            .where(PlantModel.id == plant_id)
            .values(
                current_stage=stage.value,
                total_drops=total_drops,
                drops_in_stage=drops_in_stage,
            )
        )
        await self._session.execute(stmt)

    async def increment_drops(
        self, plant_id: UUID, amount: int
    ) -> None:
        stmt = (
            update(PlantModel)
            .where(PlantModel.id == plant_id)
            .values(
                total_drops=PlantModel.total_drops + amount,
            )
        )
        await self._session.execute(stmt)
