import asyncio
import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from redis.asyncio import Redis

from src.api.middleware.auth import require_auth
from src.core.config.settings import settings

router = APIRouter(prefix="/api/events", tags=["events"])


async def event_generator(user_id: str):
    redis = Redis.from_url(settings.redis_url)
    pubsub = redis.pubsub()
    channel = f"events:user:{user_id}"
    await pubsub.subscribe(channel)

    try:
        # Send initial connection event
        yield f"data: {json.dumps({'event': 'connected', 'data': {}})}\n\n"

        while True:
            msg = await pubsub.get_message(
                timeout=30.0, ignore_subscribe_messages=True
            )
            if msg and msg["type"] == "message":
                data = msg["data"]
                if isinstance(data, bytes):
                    data = data.decode()
                yield f"data: {data}\n\n"
            # Send keepalive comment every 30s if no message
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        pass
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.close()
        await redis.close()


@router.get("/stream")
async def sse_stream(
    user_id: str = Depends(require_auth),
):
    return StreamingResponse(
        event_generator(user_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
