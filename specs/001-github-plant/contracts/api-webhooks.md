# Webhook API Contracts

## POST /api/webhooks/github

Receive GitHub webhook events (push, pull_request).

**Headers** (set by GitHub):
| Header | Description |
|--------|-------------|
| `X-GitHub-Event` | Event type (`push`, `pull_request`) |
| `X-Hub-Signature-256` | HMAC-SHA256 signature for verification |
| `X-GitHub-Delivery` | Unique delivery ID (idempotency key) |

**Request Body**: Full GitHub webhook payload (JSON)

**Processing Flow**:
1. Verify HMAC-SHA256 signature using stored webhook secret
2. Check `X-GitHub-Delivery` against processed deliveries (idempotency)
3. Enqueue processing job to Redis queue
4. Return 200 immediately — async worker handles persistence

**Response**: `202 Accepted`
```json
{
  "status": "queued",
  "delivery_id": "abc-123-def"
}
```

**Error Responses**:
- `400` — Invalid signature or malformed payload
- `429` — Too many requests (rate limiting)

---

## Webhook Events Processed

| Event | Trigger | Drop Awarded |
|-------|---------|--------------|
| `push` | Any branch push with commits | 1 drop per commit |
| `pull_request` (closed + merged) | PR merged to default branch | 1 drop per merged PR |
| Other events | Ignored | No drop |

---

## WebSocket / Events

Frontend subscribes to real-time plant updates via Server-Sent Events (SSE).

### GET /api/events/stream

SSE stream for authenticated user's plant events.

**Headers**: `Authorization: Bearer <session_token>`

**Event Types**:

**`drop_received`** — New water drop awarded
```json
{
  "event": "drop_received",
  "data": {
    "drop_id": "uuid",
    "event_type": "commit",
    "source_repo": "octocat/hello-world",
    "total_drops": 23,
    "committed_at": "2026-05-22T12:00:00Z"
  }
}
```

**`stage_advanced`** — Plant grew to next stage
```json
{
  "event": "stage_advanced",
  "data": {
    "plant_id": "uuid",
    "previous_stage": 2,
    "previous_stage_name": "sprout",
    "current_stage": 3,
    "current_stage_name": "young",
    "total_drops": 15
  }
}
```
