# Data Model: GitHub Plant Gamification

## Entities

### User

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | UUID | PK, auto-generated | Internal identifier |
| `github_id` | INTEGER | UNIQUE, NOT NULL | GitHub user ID |
| `username` | VARCHAR(39) | UNIQUE, NOT NULL | GitHub username |
| `display_name` | VARCHAR(255) | NULLABLE | GitHub display name |
| `avatar_url` | VARCHAR(512) | NULLABLE | GitHub avatar URL |
| `encrypted_token` | BYTEA | NOT NULL | AES-256-GCM encrypted GitHub OAuth token |
| `token_nonce` | BYTEA | NOT NULL | Encryption nonce |
| `github_connected_at` | TIMESTAMPTZ | NOT NULL | When OAuth was completed |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

**Validation**: 
- `username` must match GitHub username regex: `^[a-zA-Z0-9]([a-zA-Z0-9-]{0,37}[a-zA-Z0-9])?$`
- Token must be encrypted before storage (Constitution V)

---

### Plant

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | UUID | PK, auto-generated | |
| `user_id` | UUID | FK → User.id, UNIQUE, NOT NULL | One plant per user |
| `plant_type` | VARCHAR(50) | NOT NULL | `cactus`, `bonsai`, `cannabis`, `fruit` |
| `current_stage` | INTEGER | NOT NULL, DEFAULT 1 | 1=seed, 2=sprout, 3=young, 4=mature, 5=bloomed |
| `total_drops` | INTEGER | NOT NULL, DEFAULT 0 | Lifetime drops accumulated |
| `drops_in_stage` | INTEGER | NOT NULL, DEFAULT 0 | Drops since last stage advance |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

**Validation**:
- `current_stage` ∈ {1, 2, 3, 4, 5}
- `total_drops` ≥ 0, `drops_in_stage` ≥ 0
- `total_drops` = sum of drops across all past stages + `drops_in_stage` (derived, but stored for query efficiency)
- `plant_type` must be one of the defined types in `plant_types` config

---

### Drop

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | UUID | PK, auto-generated | |
| `plant_id` | UUID | FK → Plant.id, NOT NULL | |
| `event_type` | VARCHAR(50) | NOT NULL | `commit`, `pull_request_merge` |
| `source_repo` | VARCHAR(255) | NOT NULL | `owner/repo` format |
| `github_event_id` | VARCHAR(64) | UNIQUE, NOT NULL | GitHub delivery ID for idempotency |
| `committed_at` | TIMESTAMPTZ | NOT NULL | Author timestamp from GitHub |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | When processed by our system |

**Validation**:
- `github_event_id` unique — prevents duplicate drops from webhook retries
- `event_type` ∈ {`commit`, `pull_request_merge`}
- `source_repo` format: `^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$`

---

### PlantTypeConfig

Not a database table — defined as application config (JSON/YAML) in `backend/src/core/config/plant_types/`.

```yaml
plant_types:
  cactus:
    name: "Cactus"
    description: "Resilient and low-maintenance"
    stages:
      seed:     { threshold: 0,   asset: "cactus-seed.svg" }
      sprout:   { threshold: 5,   asset: "cactus-sprout.svg" }
      young:    { threshold: 15,  asset: "cactus-young.svg" }
      mature:   { threshold: 30,  asset: "cactus-mature.svg" }
      bloomed:  { threshold: 50,  asset: "cactus-bloomed.svg" }
  bonsai:
    name: "Bonsai"
    description: "Patience and discipline"
    stages:
      seed:     { threshold: 0,   asset: "bonsai-seed.svg" }
      sprout:   { threshold: 5,   asset: "bonsai-sprout.svg" }
      young:    { threshold: 15,  asset: "bonsai-young.svg" }
      mature:   { threshold: 30,  asset: "bonsai-mature.svg" }
      bloomed:  { threshold: 50,  asset: "bonsai-bloomed.svg" }
  cannabis:
    name: "Cannabis"
    description: "Fast-growing and vibrant"
    stages:
      seed:     { threshold: 0,   asset: "cannabis-seed.svg" }
      sprout:   { threshold: 5,   asset: "cannabis-sprout.svg" }
      young:    { threshold: 15,  asset: "cannabis-young.svg" }
      mature:   { threshold: 30,  asset: "cannabis-mature.svg" }
      bloomed:  { threshold: 50,  asset: "cannabis-bloomed.svg" }
  fruit:
    name: "Fruit Plant"
    description: "Bears fruit from your hard work"
    stages:
      seed:     { threshold: 0,   asset: "fruit-seed.svg" }
      sprout:   { threshold: 5,   asset: "fruit-sprout.svg" }
      young:    { threshold: 15,  asset: "fruit-young.svg" }
      mature:   { threshold: 30,  asset: "fruit-mature.svg" }
      bloomed:  { threshold: 50,  asset: "fruit-bloomed.svg" }
```

---

## Relationships

```text
User (1) ──── (1) Plant (1) ──── (N) Drop
  │                                  │
  │                                  └── event_type, source_repo, committed_at
  │
  └── github_id, username, encrypted_token
```

- One **User** has exactly one **Plant** (created on plant selection)
- One **Plant** has many **Drops** (one per commit/PR merge)
- **PlantTypeConfig** is static config, not stored per user

---

## State Machine: Plant Growth Stages

```
seed (1) ──[5 drops]──→ sprout (2) ──[15 drops]──→ young (3)
    │                                                    │
    │                                                    │
    └──────────────────[30 drops]────────────────────────┘
                              │
                              ▼
                         mature (4) ──[50 drops]──→ bloomed (5)
```

- Transitions are **unidirectional** (forward only — no regression)
- When total drops cross the threshold for the next stage, `current_stage` increments and `drops_in_stage` resets to 0
- At `bloomed` (stage 5): drops still accumulate and display but no further visual change
- Zero-width stages: if initial import grants enough drops to skip intermediate stages,
  the plant advances through each skipped stage sequentially (animations play fast-forward)

**Growth calculation algorithm**:
```
for each stage in plant_types[type].stages (ordered by ordinal):
    if total_drops >= stage.threshold:
        current_stage = stage.ordinal
        drops_in_stage = total_drops - last_stage.threshold
```

---

## Indexes

| Table | Index | Columns | Type | Purpose |
|-------|-------|---------|------|---------|
| `user` | `idx_user_github_id` | `github_id` | UNIQUE | OAuth lookup |
| `user` | `idx_user_username` | `username` | UNIQUE | Display lookup |
| `plant` | `idx_plant_user` | `user_id` | UNIQUE | User→Plant query |
| `drop` | `idx_drop_plant` | `plant_id` | BTREE | Plant drop history |
| `drop` | `idx_drop_github_event` | `github_event_id` | UNIQUE | Idempotency key |
| `drop` | `idx_drop_created_at` | `plant_id, created_at DESC` | COMPOSITE | Timeline queries |
