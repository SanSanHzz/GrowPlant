from fastapi import APIRouter, HTTPException, Request

from src.api.schemas.webhooks import WebhookResponse
from src.infrastructure.github.webhook_verification import verify_signature
from src.infrastructure.queue.redis_queue import enqueue_event

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


@router.post("/github", response_model=WebhookResponse)
async def github_webhook(request: Request):
    body = await request.body()

    sig = request.headers.get("X-Hub-Signature-256", "")
    if not sig or not verify_signature(body, sig):
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_type = request.headers.get("X-GitHub-Event", "")
    delivery_id = request.headers.get("X-GitHub-Delivery", "")

    if event_type not in ("push", "pull_request"):
        return WebhookResponse(status="ignored", delivery_id=delivery_id)

    import json
    payload = json.loads(body)

    event_data = {
        "delivery_id": delivery_id,
        "event_type": event_type,
        "payload": payload,
    }

    await enqueue_event(event_data)

    return WebhookResponse(status="queued", delivery_id=delivery_id)
