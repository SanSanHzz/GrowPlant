from pathlib import Path

import yaml

_STAGES = ["seed", "sprout", "young", "mature", "bloomed"]


def _validate_stages(plant_id: str, stages: dict) -> None:
    for name in _STAGES:
        if name not in stages:
            raise ValueError(f"Plant '{plant_id}' missing stage '{name}'")
        entry = stages[name]
        if "threshold" not in entry:
            raise ValueError(
                f"Plant '{plant_id}' stage '{name}' missing 'threshold'"
            )


def load_plant_types() -> dict:
    path = Path(__file__).parent / "plant_types.yml"
    if not path.exists():
        return _default_plant_types()

    with open(path) as f:
        data = yaml.safe_load(f)

    plants = data.get("plant_types", {})
    for pid, cfg in plants.items():
        _validate_stages(pid, cfg.get("stages", {}))

    return plants


def _default_plant_types() -> dict:
    return {
        "cactus": {
            "name": "Cactus",
            "description": "Resilient and low-maintenance",
            "stages": {
                "seed": {"threshold": 0, "asset": "cactus-seed.svg"},
                "sprout": {"threshold": 5, "asset": "cactus-sprout.svg"},
                "young": {"threshold": 15, "asset": "cactus-young.svg"},
                "mature": {"threshold": 30, "asset": "cactus-mature.svg"},
                "bloomed": {"threshold": 50, "asset": "cactus-bloomed.svg"},
            },
        },
        "bonsai": {
            "name": "Bonsai",
            "description": "Patience and discipline",
            "stages": {
                "seed": {"threshold": 0, "asset": "bonsai-seed.svg"},
                "sprout": {"threshold": 5, "asset": "bonsai-sprout.svg"},
                "young": {"threshold": 15, "asset": "bonsai-young.svg"},
                "mature": {"threshold": 30, "asset": "bonsai-mature.svg"},
                "bloomed": {"threshold": 50, "asset": "bonsai-bloomed.svg"},
            },
        },
        "cannabis": {
            "name": "Cannabis",
            "description": "Fast-growing and vibrant",
            "stages": {
                "seed": {"threshold": 0, "asset": "cannabis-seed.svg"},
                "sprout": {"threshold": 5, "asset": "cannabis-sprout.svg"},
                "young": {"threshold": 15, "asset": "cannabis-young.svg"},
                "mature": {"threshold": 30, "asset": "cannabis-mature.svg"},
                "bloomed": {"threshold": 50, "asset": "cannabis-bloomed.svg"},
            },
        },
        "fruit": {
            "name": "Fruit Plant",
            "description": "Bears fruit from your hard work",
            "stages": {
                "seed": {"threshold": 0, "asset": "fruit-seed.svg"},
                "sprout": {"threshold": 5, "asset": "fruit-sprout.svg"},
                "young": {"threshold": 15, "asset": "fruit-young.svg"},
                "mature": {"threshold": 30, "asset": "fruit-mature.svg"},
                "bloomed": {"threshold": 50, "asset": "fruit-bloomed.svg"},
            },
        },
    }


PLANT_TYPES = load_plant_types()
