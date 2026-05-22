# Dashboard API Contracts

## GET /api/dashboard

Full dashboard state — combines plant, drops, and progress.

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
    "stage_progress_pct": 46.7,
    "max_stage_reached": false
  },
  "recent_drops": [
    {
      "id": "uuid",
      "event_type": "commit",
      "source_repo": "octocat/hello-world",
      "committed_at": "2026-05-22T11:30:00Z",
      "created_at": "2026-05-22T11:31:00Z"
    }
  ],
  "stats": {
    "total_commits": 20,
    "total_pr_merges": 2,
    "repositories_contributing": ["octocat/hello-world", "octocat/another-repo"],
    "first_drop_at": "2026-05-01T00:00:00Z",
    "last_drop_at": "2026-05-22T11:31:00Z"
  }
}
```

**Query Parameters**:
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `limit` | integer | 20 | Max recent drops to return |

---

## GET /api/dashboard/history

Paginated drop history.

**Headers**: `Authorization: Bearer <session_token>`

**Query Parameters**:
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `cursor` | string | null | Pagination cursor (opaque) |
| `limit` | integer | 50 | Page size |

**Response**: `200 OK`
```json
{
  "drops": [
    {
      "id": "uuid",
      "event_type": "commit",
      "source_repo": "octocat/hello-world",
      "committed_at": "2026-05-22T11:30:00Z",
      "created_at": "2026-05-22T11:31:00Z"
    }
  ],
  "next_cursor": "opaque-cursor-string",
  "has_more": true,
  "total_drops": 142
}
```
