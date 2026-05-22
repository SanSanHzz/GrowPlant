from src.core.config.plant_types.loader import PLANT_TYPES
from src.core.entities.plant import STAGE_NAMES, GrowthStage, Plant


class PlantGrowthService:

    @staticmethod
    def get_stage_thresholds(plant_type: str) -> list[dict]:
        config = PLANT_TYPES.get(plant_type)
        if not config:
            raise ValueError(f"Unknown plant type: {plant_type}")
        stages = config["stages"]
        ordered = []
        for name in STAGE_NAMES.values():
            if name in stages:
                ordered.append(stages[name])
        return ordered

    @staticmethod
    def calculate_stage(
        total_drops: int, plant_type: str
    ) -> tuple[GrowthStage, int]:
        thresholds = PlantGrowthService.get_stage_thresholds(plant_type)
        current = GrowthStage.SEED
        prev_threshold = 0

        for i, stage in enumerate(thresholds):
            if total_drops >= stage["threshold"]:
                current = GrowthStage(i + 1)
                prev_threshold = stage["threshold"]

        drops_in_stage = total_drops - prev_threshold
        return current, drops_in_stage

    @staticmethod
    def check_stage_transition(
        plant: Plant, new_total_drops: int
    ) -> tuple[GrowthStage, GrowthStage, bool]:
        new_stage, _ = PlantGrowthService.calculate_stage(
            new_total_drops, plant.plant_type.value
        )
        old_stage = plant.current_stage
        return old_stage, new_stage, new_stage > old_stage
