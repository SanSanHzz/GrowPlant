# Plants API Contracts

## GET /api/plants/types

List available plant types with preview info.

**Headers**: `Authorization: Bearer <session_token>`

**Response**: `200 OK`
```json
{
  "plant_types": [
    {
      "id": "cactus",
      "name": "Cactus",
      "description": "Resilient and low-maintenance",
      "preview_image": "/static/plants/cactus-preview.svg"
    },
    {
      "id": "bonsai",
      "name": "Bonsai",
      "description": "Patience and discipline",
      "preview_image": "/static/plants/bonsai-preview.svg"
    },
    {
      "id": "cannabis",
      "name": "Cannabis",
      "description": "Fast-growing and vibrant",
      "preview_image": "/static/plants/cannabis-preview.svg"
    },
    {
      "id": "fruit",
      "name": "Fruit Plant",
      "description": "Bears fruit from your hard work",
      "preview_image": "/static/plants/fruit-preview.svg"
    }
  ]
}
```

---

## POST /api/plants/select

Select plant type after first authentication.

**Headers**: `Authorization: Bearer <session_token>`

**Request Body**:
```json
{
  "plant_type": "cactus"
}
```

**Validation**: `plant_type` must be one of the valid plant type IDs.

**Response**: `201 Created`
```json
{
  "plant": {
    "id": "uuid",
    "plant_type": "cactus",
    "current_stage": 1,
    "current_stage_name": "seed",
    "total_drops": 0,
    "drops_to_next_stage": 5,
    "created_at": "2026-05-22T00:00:00Z"
  }
}
```

**Error Responses**:
- `400` — Invalid plant type
- `409` — User already has a plant selected

---

## GET /api/plants/mine

Get current user's plant state.

**Headers**: `Authorization: Bearer <session_token>`

**Response**: `200 OK`
```json
{
  "plant": {
    "id": "uuid",
    "plant_type": "cactus",
    "current_stage": 3,
    "current_stage_name": "young",
    "total_drops": 22,
    "drops_in_stage": 7,
    "drops_to_next_stage": 8,
    "created_at": "2026-05-22T00:00:00Z",
    "updated_at": "2026-05-22T12:00:00Z"
  }
}
```

**Error Responses**:
- `404` — User has not selected a plant yet
