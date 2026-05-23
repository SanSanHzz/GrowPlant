from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entities.drop import Drop, DropEventType
from src.core.ports.drop_repository import DropRepository
from src.infrastructure.database.models.drop import DropModel


class PostgresDropRepository(DropRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_entity(model: DropModel) -> Drop:
        return Drop(
            id=model.id,
            plant_id=model.plant_id,
            event_type=DropEventType(model.event_type),
            source_repo=model.source_repo,
            github_event_id=model.github_event_id,
            committed_at=model.committed_at,
            created_at=model.created_at,
        )

    async def create(
        self,
        plant_id: UUID,
        event_type: str | DropEventType,
        source_repo: str,
        github_event_id: str,
        committed_at: object,
    ) -> Drop:
        model = DropModel(
            plant_id=plant_id,
            event_type=event_type.value if isinstance(event_type, DropEventType) else event_type,
            source_repo=source_repo,
            github_event_id=github_event_id,
            committed_at=committed_at,
        )
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def exists_by_github_event_id(
        self, github_event_id: str
    ) -> bool:
        stmt = select(
            select(DropModel).where(
                DropModel.github_event_id == github_event_id
            ).exists()
        )
        result = await self._session.execute(stmt)
        return result.scalar() or False

    async def list_by_plant_id(
        self,
        plant_id: UUID,
        limit: int = 20,
        cursor: str | None = None,
    ) -> tuple[list[Drop], str | None]:
        stmt = (
            select(DropModel)
            .where(DropModel.plant_id == plant_id)
            .order_by(DropModel.committed_at.desc())
            .limit(limit + 1)
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        has_more = len(models) > limit
        if has_more:
            models = models[:limit]
        drops = [self._to_entity(m) for m in models]
        next_cursor = (
            str(drops[-1].id) if has_more and drops else None
        )
        return drops, next_cursor
