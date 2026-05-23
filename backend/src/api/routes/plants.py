from fastapi import APIRouter, Depends, HTTPException

from src.api.middleware.auth import require_auth
from src.api.schemas.plants import (
    PlantResponse,
    PlantSelectRequest,
    PlantTypeResponse,
)
from src.core.config.plant_types.loader import PLANT_TYPES
from src.core.entities.plant import PlantType as PlantTypeEnum
from src.core.services.plant_growth import PlantGrowthService
from src.infrastructure.database.engine import async_session_factory
from src.infrastructure.database.repositories.plant_repository import (
    PostgresPlantRepository,
)

router = APIRouter(prefix="/api/plants", tags=["plants"])

STAGE_NAMES = ["seed", "sprout", "young", "mature", "bloomed"]


@router.get("/types", response_model=list[PlantTypeResponse])
async def list_plant_types():
    return [
        PlantTypeResponse(
            id=pid,
            name=cfg["name"],
            description=cfg["description"],
            preview_image=f"/static/plants/{pid}-preview.svg",
        )
        for pid, cfg in PLANT_TYPES.items()
    ]


@router.post("/select", response_model=PlantResponse)
async def select_plant(
    body: PlantSelectRequest,
    user_id: str = Depends(require_auth),
):
    if body.plant_type not in PLANT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid plant type. Choose from: {list(PLANT_TYPES.keys())}",
        )

    from uuid import UUID
    uid = UUID(user_id)

    async with async_session_factory() as session:
        repo = PostgresPlantRepository(session)
        existing = await repo.get_by_user_id(uid)
        if existing:
            raise HTTPException(
                status_code=409,
                detail="User already has a plant selected",
            )

        plant = await repo.create(uid, PlantTypeEnum(body.plant_type))
        thresholds = PlantGrowthService.get_stage_thresholds(
            body.plant_type
        )
        next_threshold = (
            thresholds[1]["threshold"] if len(thresholds) > 1 else 0
        )

    return PlantResponse(
        id=plant.id,
        plant_type=plant.plant_type.value,
        current_stage=plant.current_stage.value,
        current_stage_name=STAGE_NAMES[0],
        total_drops=plant.total_drops,
        drops_to_next_stage=next_threshold,
        created_at=str(plant.created_at),
    )


@router.get("/mine", response_model=PlantResponse)
async def get_my_plant(
    user_id: str = Depends(require_auth),
):
    from uuid import UUID
    uid = UUID(user_id)

    async with async_session_factory() as session:
        repo = PostgresPlantRepository(session)
        plant = await repo.get_by_user_id(uid)
        if not plant:
            raise HTTPException(
                status_code=404,
                detail="No plant selected yet",
            )

        thresholds = PlantGrowthService.get_stage_thresholds(
            plant.plant_type.value
        )
        stage_idx = plant.current_stage.value - 1
        next_threshold = (
            thresholds[stage_idx + 1]["threshold"]
            if stage_idx + 1 < len(thresholds)
            else plant.total_drops
        )

    return PlantResponse(
        id=plant.id,
        plant_type=plant.plant_type.value,
        current_stage=plant.current_stage.value,
        current_stage_name=STAGE_NAMES[plant.current_stage.value - 1],
        total_drops=plant.total_drops,
        drops_to_next_stage=max(0, next_threshold - plant.total_drops),
        created_at=str(plant.created_at),
    )
