import json

from redis.asyncio import Redis

from src.core.config.settings import settings

QUEUE_KEY = "webhook:events"
redis_client: Redis | None = None


async def get_redis() -> Redis:
    global redis_client
    if redis_client is None:
        redis_client = Redis.from_url(settings.redis_url)
    return redis_client


async def enqueue_event(payload: dict) -> None:
    r = await get_redis()
    await r.rpush(QUEUE_KEY, json.dumps(payload))


async def dequeue_event() -> dict | None:
    r = await get_redis()
    raw = await r.lpop(QUEUE_KEY)
    if raw is None:
        return None
    return json.loads(raw)
