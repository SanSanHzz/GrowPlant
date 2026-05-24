from fastapi import APIRouter, Depends, HTTPException

from src.api.middleware.auth import require_auth
from src.api.schemas.plants import (
    PlantTypeResponse,
    PlantSelectRequest,
    PlantActivateRequest,
    PlantRenameRequest,
    PlantResponse,
    PlantListResponse,
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


def _plant_to_response(plant) -> PlantResponse:
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
        name=plant.name,
        is_active=plant.is_active,
        created_at=str(plant.created_at),
    )


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
        plants = await repo.list_by_user_id(uid)
        is_first = len(plants) == 0

        plant = await repo.create(
            uid, PlantTypeEnum(body.plant_type), is_active=is_first
        )
        await session.commit()

    return _plant_to_response(plant)


@router.get("/mine", response_model=PlantListResponse)
async def list_my_plants(
    user_id: str = Depends(require_auth),
):
    from uuid import UUID
    uid = UUID(user_id)

    async with async_session_factory() as session:
        repo = PostgresPlantRepository(session)
        plants = await repo.list_by_user_id(uid)

    active = next((p for p in plants if p.is_active), None)
    return PlantListResponse(
        plants=[_plant_to_response(p) for p in plants],
        active_plant_id=active.id if active else None,
    )


@router.post("/activate", response_model=PlantResponse)
async def activate_plant(
    body: PlantActivateRequest,
    user_id: str = Depends(require_auth),
):
    from uuid import UUID
    uid = UUID(user_id)

    async with async_session_factory() as session:
        repo = PostgresPlantRepository(session)
        plant = await repo.get_by_id(body.plant_id)
        if not plant or plant.user_id != uid:
            raise HTTPException(status_code=404, detail="Plant not found")

        await repo.set_active(body.plant_id, uid)
        await session.commit()

        plant = await repo.get_by_id(body.plant_id)
        assert plant is not None

    return _plant_to_response(plant)


@router.patch("/{plant_id}/name", response_model=PlantResponse)
async def rename_plant(
    plant_id: str,
    body: PlantRenameRequest,
    user_id: str = Depends(require_auth),
):
    from uuid import UUID
    uid = UUID(user_id)
    pid = UUID(plant_id)

    async with async_session_factory() as session:
        repo = PostgresPlantRepository(session)
        plant = await repo.get_by_id(pid)
        if not plant or plant.user_id != uid:
            raise HTTPException(status_code=404, detail="Plant not found")

        if not body.name.strip():
            raise HTTPException(status_code=400, detail="Name cannot be empty")

        await repo.update_name(pid, body.name.strip())
        await session.commit()

        plant = await repo.get_by_id(pid)
        assert plant is not None

    return _plant_to_response(plant)


@router.delete("/{plant_id}")
async def delete_plant(
    plant_id: str,
    user_id: str = Depends(require_auth),
):
    from uuid import UUID
    uid = UUID(user_id)
    pid = UUID(plant_id)

    async with async_session_factory() as session:
        repo = PostgresPlantRepository(session)
        plant = await repo.get_by_id(pid)
        if not plant or plant.user_id != uid:
            raise HTTPException(status_code=404, detail="Plant not found")

        await repo.delete(pid)
        await session.commit()

        # If we deleted the active plant, activate another one
        remaining = await repo.list_by_user_id(uid)
        if plant.is_active and remaining:
            await repo.set_active(remaining[0].id, uid)
            await session.commit()

    return {"detail": "Plant deleted"}
