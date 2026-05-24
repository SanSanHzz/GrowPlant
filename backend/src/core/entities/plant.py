from dataclasses import dataclass
from enum import IntEnum, StrEnum
from uuid import UUID


class PlantType(StrEnum):
    CACTUS = "cactus"
    BONSAI = "bonsai"
    CANNABIS = "cannabis"
    FRUIT = "fruit"


class GrowthStage(IntEnum):
    SEED = 1
    SPROUT = 2
    YOUNG = 3
    MATURE = 4
    BLOOMED = 5


STAGE_NAMES = {
    GrowthStage.SEED: "seed",
    GrowthStage.SPROUT: "sprout",
    GrowthStage.YOUNG: "young",
    GrowthStage.MATURE: "mature",
    GrowthStage.BLOOMED: "bloomed",
}


@dataclass
class Plant:
    id: UUID
    user_id: UUID
    plant_type: PlantType
    current_stage: GrowthStage
    total_drops: int
    drops_in_stage: int
    name: str | None
    is_active: bool
    created_at: object
    updated_at: object
