from uuid import UUID

from pydantic import BaseModel


class PlantTypeResponse(BaseModel):
    id: str
    name: str
    description: str
    preview_image: str


class PlantSelectRequest(BaseModel):
    plant_type: str


class PlantActivateRequest(BaseModel):
    plant_id: UUID


class PlantRenameRequest(BaseModel):
    name: str


class PlantResponse(BaseModel):
    id: UUID
    plant_type: str
    current_stage: int
    current_stage_name: str
    total_drops: int
    drops_to_next_stage: int
    name: str | None
    is_active: bool
    created_at: str

    model_config = {"from_attributes": True}


class PlantListResponse(BaseModel):
    plants: list[PlantResponse]
    active_plant_id: UUID | None
