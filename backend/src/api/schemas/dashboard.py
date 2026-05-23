from uuid import UUID

from pydantic import BaseModel


class PlantStateResponse(BaseModel):
    id: UUID
    plant_type: str
    current_stage: int
    current_stage_name: str
    total_drops: int
    drops_in_stage: int
    drops_to_next_stage: int
    stage_progress_pct: float
    max_stage_reached: bool

    model_config = {"from_attributes": True}


class DropItemResponse(BaseModel):
    id: UUID
    event_type: str
    source_repo: str
    committed_at: str
    created_at: str

    model_config = {"from_attributes": True}


class DashboardResponse(BaseModel):
    plant: PlantStateResponse | None
    recent_drops: list[DropItemResponse]
    stats: dict


class DropHistoryResponse(BaseModel):
    drops: list[DropItemResponse]
    next_cursor: str | None
    has_more: bool
    total_drops: int
