"""arq background worker — processes webhook events from Redis queue."""


from redis.asyncio import Redis

from src.core.config.settings import settings
from src.core.services.plant_growth import PlantGrowthService
from src.infrastructure.database.engine import async_session_factory
from src.infrastructure.database.repositories.drop_repository import (
    PostgresDropRepository,
)
from src.infrastructure.database.repositories.plant_repository import (
    PostgresPlantRepository,
)
from src.infrastructure.database.repositories.user_repository import (
    PostgresUserRepository,
)

WEBHOOK_QUEUE = "webhook:events"


async def process_webhook(ctx: dict, event_data: dict) -> None:
    """Process a single webhook event: persist drops + recalculate stage."""
    delivery_id = event_data.get("delivery_id", "")
    event_type = event_data.get("event_type", "")
    payload = event_data.get("payload", {})

    if event_type not in ("push", "pull_request"):
        return

    repo_full = (
        payload.get("repository", {}).get("full_name", "unknown/unknown")
    )

    async with async_session_factory() as session:
        drop_repo = PostgresDropRepository(session)

        if event_type == "push":
            commits = payload.get("commits", [])
            for commit in commits:
                ghe_id = f"{delivery_id}-commit-{commit.get('id', '')}"
                if await drop_repo.exists_by_github_event_id(ghe_id):
                    continue

                sender = payload.get("sender", {})
                gh_login = sender.get("login", "")
                if not gh_login:
                    continue

                user_repo = PostgresUserRepository(session)
                user = await user_repo.get_by_username(gh_login)
                if not user:
                    continue

                plant_repo = PostgresPlantRepository(session)
                plant = await plant_repo.get_by_user_id(user.id)
                if not plant:
                    continue

                await drop_repo.create(
                    plant_id=plant.id,
                    event_type="commit",
                    source_repo=repo_full,
                    github_event_id=ghe_id,
                    committed_at=commit.get("timestamp"),
                )

                new_total = plant.total_drops + 1
                old_stage, new_stage, changed = (
                    PlantGrowthService.check_stage_transition(
                        plant, new_total
                    )
                )
                _, drops_in_stage = PlantGrowthService.calculate_stage(
                    new_total, plant.plant_type.value
                )
                await plant_repo.update_stage(
                    plant.id, new_stage, new_total, drops_in_stage
                )

        elif event_type == "pull_request":
            pr = payload.get("pull_request", {})
            if not pr.get("merged", False):
                return

            ghe_id = f"{delivery_id}-pr-{pr.get('id', '')}"
            if await drop_repo.exists_by_github_event_id(ghe_id):
                return

            sender = payload.get("sender", {})
            gh_login = sender.get("login", "")
            if not gh_login:
                return

            user_repo = PostgresUserRepository(session)
            user = await user_repo.get_by_username(gh_login)
            if not user:
                return

            plant_repo = PostgresPlantRepository(session)
            plant = await plant_repo.get_by_user_id(user.id)
            if not plant:
                return

            await drop_repo.create(
                plant_id=plant.id,
                event_type="pull_request_merge",
                source_repo=repo_full,
                github_event_id=ghe_id,
                committed_at=pr.get("merged_at"),
            )

            new_total = plant.total_drops + 1
            old_stage, new_stage, changed = (
                PlantGrowthService.check_stage_transition(
                    plant, new_total
                )
            )
            _, drops_in_stage = PlantGrowthService.calculate_stage(
                new_total, plant.plant_type.value
            )
            await plant_repo.update_stage(
                plant.id, new_stage, new_total, drops_in_stage
            )

        await session.commit()


async def startup(ctx: dict) -> None:
    ctx["redis"] = Redis.from_url(settings.redis_url)


async def shutdown(ctx: dict) -> None:
    await ctx["redis"].close()


class WorkerSettings:
    functions = [process_webhook]
    redis_settings = settings.redis_url
    on_startup = startup
    on_shutdown = shutdown
    queue_name = WEBHOOK_QUEUE
