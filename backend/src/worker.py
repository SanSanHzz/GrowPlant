"""Background worker — processes webhook events from Redis queue."""

import asyncio
import json
import logging
from datetime import datetime, timezone
from uuid import UUID

from redis.asyncio import Redis as AsyncRedis

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
logger = logging.getLogger("growplant.worker")


async def _publish(redis: AsyncRedis, user_id: UUID, event: str, data: dict) -> None:
    channel = f"events:user:{user_id}"
    payload = json.dumps({"event": event, "data": data})
    await redis.publish(channel, payload)


async def process_event(event_data: dict) -> None:
    delivery_id = event_data.get("delivery_id", "")
    event_type = event_data.get("event_type", "")
    payload = event_data.get("payload", {})

    if event_type not in ("push", "pull_request"):
        return

    repo_full = payload.get("repository", {}).get("full_name", "unknown/unknown")

    async with async_session_factory() as session:
        drop_repo = PostgresDropRepository(session)
        user_repo = PostgresUserRepository(session)
        plant_repo = PostgresPlantRepository(session)

        sender = payload.get("sender", {})
        gh_login = sender.get("login", "")
        if not gh_login:
            return

        user = await user_repo.get_by_username(gh_login)
        if not user:
            return

        plant = await plant_repo.get_active(user.id)
        if not plant:
            return

        events_published: list[tuple[str, dict]] = []

        if event_type == "push":
            commits = payload.get("commits", [])
            for commit in commits:
                ghe_id = f"{delivery_id}-commit-{commit.get('id', '')}"
                if await drop_repo.exists_by_github_event_id(ghe_id):
                    continue

                ts = commit.get("timestamp")
                if isinstance(ts, str):
                    ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                await drop_repo.create(
                    plant_id=plant.id,
                    event_type="commit",
                    source_repo=repo_full,
                    github_event_id=ghe_id,
                    committed_at=ts,
                )

                new_total = plant.total_drops + 1
                old_stage, new_stage, changed = PlantGrowthService.check_stage_transition(
                    plant, new_total
                )
                _, drops_in_stage = PlantGrowthService.calculate_stage(
                    new_total, plant.plant_type.value
                )
                await plant_repo.update_stage(plant.id, new_stage, new_total, drops_in_stage)
                plant.total_drops = new_total
                plant.current_stage = new_stage

                events_published.append(
                    ("drop_received", {"total_drops": new_total, "source_repo": repo_full})
                )
                if changed:
                    events_published.append(
                        (
                            "stage_advanced",
                            {
                                "previous_stage": old_stage.value,
                                "new_stage": new_stage.value,
                                "total_drops": new_total,
                            },
                        )
                    )

        elif event_type == "pull_request":
            pr = payload.get("pull_request", {})
            if not pr.get("merged", False):
                return

            ghe_id = f"{delivery_id}-pr-{pr.get('id', '')}"
            if await drop_repo.exists_by_github_event_id(ghe_id):
                return

            ts = pr.get("merged_at")
            if isinstance(ts, str):
                ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            await drop_repo.create(
                plant_id=plant.id,
                event_type="pull_request_merge",
                source_repo=repo_full,
                github_event_id=ghe_id,
                committed_at=ts,
            )

            new_total = plant.total_drops + 1
            old_stage, new_stage, changed = PlantGrowthService.check_stage_transition(
                plant, new_total
            )
            _, drops_in_stage = PlantGrowthService.calculate_stage(
                new_total, plant.plant_type.value
            )
            await plant_repo.update_stage(plant.id, new_stage, new_total, drops_in_stage)

            events_published.append(
                ("drop_received", {"total_drops": new_total, "source_repo": repo_full})
            )
            if changed:
                events_published.append(
                    (
                        "stage_advanced",
                        {
                            "previous_stage": old_stage.value,
                            "new_stage": new_stage.value,
                            "total_drops": new_total,
                        },
                    )
                )

        await session.commit()

    # Publish events after session is done
    if events_published:
        r = AsyncRedis.from_url(settings.redis_url)
        for event_name, event_data in events_published:
            await _publish(r, user.id, event_name, event_data)
        await r.close()
        logger.info("Published %d events for user %s", len(events_published), user.username)


async def worker_loop():
    redis = AsyncRedis.from_url(settings.redis_url)
    logger.info("Worker started, polling queue: %s", WEBHOOK_QUEUE)
    try:
        while True:
            raw = await redis.blpop(WEBHOOK_QUEUE, timeout=5)
            if raw is None:
                continue
            _, data = raw
            try:
                event = json.loads(data)
                logger.info("Processing event: %s", event.get("delivery_id", ""))
                await process_event(event)
            except Exception as e:
                import traceback
                logger.error("Error processing event: %s\n%s", e, traceback.format_exc())
    finally:
        await redis.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    asyncio.run(worker_loop())
