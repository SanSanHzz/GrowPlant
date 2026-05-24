from fastapi import APIRouter, Depends, Query

from src.api.middleware.auth import require_auth
from src.api.schemas.dashboard import (
    DashboardResponse,
    DropHistoryResponse,
    DropItemResponse,
    PlantStateResponse,
)
from src.core.services.plant_growth import PlantGrowthService
from src.infrastructure.database.engine import async_session_factory
from src.infrastructure.database.repositories.drop_repository import (
    PostgresDropRepository,
)
from src.infrastructure.database.repositories.plant_repository import (
    PostgresPlantRepository,
)

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

STAGE_NAMES = ["seed", "sprout", "young", "mature", "bloomed"]


def _build_plant_state(plant) -> PlantStateResponse | None:
    if plant is None:
        return None
    thresholds = PlantGrowthService.get_stage_thresholds(
        plant.plant_type.value
    )
    max_stage = len(thresholds)
    stage_name = STAGE_NAMES[plant.current_stage.value - 1]

    next_threshold = None
    if plant.current_stage.value < max_stage:
        next_threshold = thresholds[plant.current_stage.value]["threshold"]
    elif plant.current_stage.value < len(thresholds):
        next_threshold = thresholds[plant.current_stage.value]["threshold"]

    pct = 100.0
    if next_threshold is not None and plant.current_stage.value > 1:
        prev_threshold = thresholds[plant.current_stage.value - 2]["threshold"]
        range_size = next_threshold - prev_threshold
        if range_size > 0:
            pct = ((plant.total_drops - prev_threshold) / range_size) * 100

    return PlantStateResponse(
        id=plant.id,
        plant_type=plant.plant_type.value,
        current_stage=plant.current_stage.value,
        current_stage_name=stage_name,
        total_drops=plant.total_drops,
        drops_in_stage=plant.drops_in_stage,
        drops_to_next_stage=(
            next_threshold - plant.total_drops
            if next_threshold and plant.total_drops < next_threshold
            else 0
        ),
        stage_progress_pct=round(min(pct, 100.0), 1),
        max_stage_reached=plant.current_stage.value >= max_stage,
    )


@router.get("", response_model=DashboardResponse)
async def get_dashboard(
    user_id: str = Depends(require_auth),
    limit: int = Query(20, ge=1, le=100),
):
    from uuid import UUID

    uid = UUID(user_id)

    async with async_session_factory() as session:
        plant_repo = PostgresPlantRepository(session)
        plant = await plant_repo.get_active(uid)

        recent_drops = []
        total_drops_count = 0
        if plant:
            drop_repo = PostgresDropRepository(session)
            drops, _ = await drop_repo.list_by_plant_id(
                plant.id, limit=limit
            )
            recent_drops = [
                DropItemResponse(
                    id=d.id,
                    event_type=d.event_type.value,
                    source_repo=d.source_repo,
                    committed_at=str(d.committed_at),
                    created_at=str(d.created_at),
                )
                for d in drops
            ]
            total_drops_count = plant.total_drops

    return DashboardResponse(
        plant=_build_plant_state(plant),
        recent_drops=recent_drops,
        stats={
            "total_commits": total_drops_count,
            "total_pr_merges": 0,
            "repositories_contributing": list(
                set(d.source_repo for d in recent_drops)
            ),
            "first_drop_at": (
                str(recent_drops[-1].committed_at)
                if recent_drops
                else None
            ),
            "last_drop_at": (
                str(recent_drops[0].committed_at)
                if recent_drops
                else None
            ),
        },
    )


@router.get("/history", response_model=DropHistoryResponse)
async def get_drop_history(
    user_id: str = Depends(require_auth),
    plant_id: str | None = Query(None),
    cursor: str | None = Query(None),
    limit: int = Query(50, ge=1, le=100),
):
    from uuid import UUID

    uid = UUID(user_id)

    async with async_session_factory() as session:
        plant_repo = PostgresPlantRepository(session)
        if plant_id:
            plant = await plant_repo.get_by_id(UUID(plant_id))
        else:
            plant = await plant_repo.get_active(uid)

        if not plant or plant.user_id != uid:
            return DropHistoryResponse(
                drops=[], next_cursor=None, has_more=False, total_drops=0
            )

        drop_repo = PostgresDropRepository(session)
        drops, next_cursor = await drop_repo.list_by_plant_id(
            plant.id, limit=limit
        )

    return DropHistoryResponse(
        drops=[
            DropItemResponse(
                id=d.id,
                event_type=d.event_type.value,
                source_repo=d.source_repo,
                committed_at=str(d.committed_at),
                created_at=str(d.created_at),
            )
            for d in drops
        ],
        next_cursor=next_cursor,
        has_more=next_cursor is not None,
        total_drops=plant.total_drops,
    )
