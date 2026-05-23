from uuid import UUID

from pydantic import BaseModel


class PlantTypeResponse(BaseModel):
    id: str
    name: str
    description: str
    preview_image: str


class PlantSelectRequest(BaseModel):
    plant_type: str


class PlantResponse(BaseModel):
    id: UUID
    plant_type: str
    current_stage: int
    current_stage_name: str
    total_drops: int
    drops_to_next_stage: int
    created_at: str

    model_config = {"from_attributes": True}
