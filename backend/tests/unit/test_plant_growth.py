import pytest

from src.core.services.plant_growth import PlantGrowthService


class TestPlantGrowthService:

    def test_seed_at_zero_drops(self):
        stage, drops = PlantGrowthService.calculate_stage(0, "cactus")
        assert stage.value == 1
        assert stage.name == "SEED"
        assert drops == 0

    def test_sprout_at_five_drops(self):
        stage, drops = PlantGrowthService.calculate_stage(5, "cactus")
        assert stage.value == 2
        assert stage.name == "SPROUT"
        assert drops == 0

    def test_young_at_twenty_drops(self):
        stage, drops = PlantGrowthService.calculate_stage(20, "cactus")
        assert stage.value == 3
        assert drops == 5

    def test_mature_at_thirty_drops(self):
        stage, drops = PlantGrowthService.calculate_stage(30, "cactus")
        assert stage.value == 4
        assert drops == 0

    def test_bloomed_at_fifty_drops(self):
        stage, drops = PlantGrowthService.calculate_stage(50, "cactus")
        assert stage.value == 5
        assert drops == 0

    def test_bloomed_above_max(self):
        stage, drops = PlantGrowthService.calculate_stage(100, "cactus")
        assert stage.value == 5
        assert drops == 50

    def test_all_plant_types_reach_bloomed(self):
        for plant_type in ("cactus", "bonsai", "cannabis", "fruit"):
            stage, _ = PlantGrowthService.calculate_stage(60, plant_type)
            assert stage.value == 5, f"{plant_type} should bloom at 60 drops"

    def test_unknown_plant_type_raises(self):
        with pytest.raises(ValueError, match="Unknown plant type"):
            PlantGrowthService.calculate_stage(10, "invalid")

    def test_check_transition_no_change(self):
        from src.core.entities.plant import Plant, PlantType, GrowthStage
        from uuid import uuid4

        plant = Plant(
            id=uuid4(),
            user_id=uuid4(),
            plant_type=PlantType.CACTUS,
            current_stage=GrowthStage.SPROUT,
            total_drops=5,
            drops_in_stage=0,
            created_at=None,
            updated_at=None,
        )
        old, new, changed = PlantGrowthService.check_stage_transition(
            plant, 6
        )
        assert changed is False
        assert old == new

    def test_check_transition_advances(self):
        from src.core.entities.plant import Plant, PlantType, GrowthStage
        from uuid import uuid4

        plant = Plant(
            id=uuid4(),
            user_id=uuid4(),
            plant_type=PlantType.CACTUS,
            current_stage=GrowthStage.SPROUT,
            total_drops=5,
            drops_in_stage=0,
            created_at=None,
            updated_at=None,
        )
        old, new, changed = PlantGrowthService.check_stage_transition(
            plant, 15
        )
        assert changed is True
        assert old == GrowthStage.SPROUT
        assert new == GrowthStage.YOUNG
