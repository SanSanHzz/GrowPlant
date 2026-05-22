<!--
  Sync Impact Report
  ==================
  Version change: N/A (placeholder) → 1.0.0
  Modified principles (all new — previously placeholders):
    - [PRINCIPLE_1_NAME] → "I. Deployment Simplicity"
    - [PRINCIPLE_2_NAME] → "II. Data Scalability"
    - [PRINCIPLE_3_NAME] → "III. Clean Architecture"
    - [PRINCIPLE_4_NAME] → "IV. Visual Modularity"
    - [PRINCIPLE_5_NAME] → "V. Security & Privacy"
  Added sections:
    - Section 2: "Technology Stack & Constraints" (formerly [SECTION_2_NAME])
    - Section 3: "Development Workflow" (formerly [SECTION_3_NAME])
    - Governance: fully populated (formerly [GOVERNANCE_RULES])
  Removed sections: None
  Templates requiring updates:
    - .specify/templates/plan-template.md        ✅ No changes needed (generic Constitution Check)
    - .specify/templates/spec-template.md        ✅ No changes needed
    - .specify/templates/tasks-template.md       ✅ No changes needed
    - .opencode/commands/*.md                    ✅ No outdated references found
    - AGENTS.md                                  ✅ No changes needed
  Follow-up TODOs: None — all placeholders filled.
-->

# GrowPlant Constitution

## Core Principles

### I. Deployment Simplicity

The application MUST be locally configurable with minimal friction.
- Setup MUST be achievable with a single configuration file (`.env` or equivalent).
- All dependencies MUST be declared explicitly (e.g., `requirements.txt`, `package.json`).
- A containerized environment (e.g., `docker-compose.yml`) MUST be provided for one-command local bootstrapping.

Rationale: Lowers the barrier to entry for contributors and self-hosters.

### II. Data Scalability

The backend MUST process GitHub webhooks asynchronously.
- Webhook payloads MUST be queued (message queue or task queue) before persisting to the database.
- Database writes MUST NOT block event ingestion — the webhook endpoint MUST return promptly.
- The system MUST degrade gracefully under burst traffic without data loss.

Rationale: GitHub can send bursts of webhook events; synchronous writes cause backpressure,
request timeouts, and potential data loss.

### III. Clean Architecture

Business logic (plant growth, drip calculation) MUST be isolated from data access and
presentation.
- Domain models MUST NOT depend on infrastructure concerns (databases, web frameworks,
  rendering libraries).
- Each layer MUST have a single, well-defined responsibility.
- Dependency direction MUST point inward: infrastructure depends on core, never the reverse.

Rationale: Enables testability, maintainability, and technology evolution without rewriting
core logic.

### IV. Visual Modularity

Plant types and their growth stages MUST be independently defined and configurable.
- Adding a new plant type MUST NOT require modifications to existing plant rendering or
  growth logic.
- Growth state definitions MUST be decoupled from rendering implementation.
- Visual components MUST be swappable per plant type without side effects.

Rationale: Allows the visual ecosystem to grow organically without cascading changes.

### V. Security & Privacy

Credentials MUST NOT be stored in plaintext.
- GitHub tokens and all secrets MUST be loaded from environment variables or a secrets
  manager — never hardcoded or committed.
- Sensible data minimization MUST be applied: collect only what is necessary for plant
  growth calculation.
- Encryption MUST be used for any persisted sensitive data.

Rationale: Protects users and the project from credential leaks and privacy violations.

## Technology Stack & Constraints

- **Backend**: MUST support async I/O for non-blocking webhook ingestion (e.g., Python
  with asyncio, Node.js, or Go).
- **Database**: PostgreSQL preferred for structured growth state; any alternative MUST
  justify transactional guarantees.
- **Frontend**: MUST be framework-agnostic — rendering layer MUST NOT couple to business
  logic.
- **Deployment**: Docker Compose MUST be provided for local development; production
  deployments SHOULD use the same container images.
- **Infrastructure**: A message queue (Redis, RabbitMQ, or equivalent) REQUIRED for
  asynchronous webhook processing.
- **Language decisions**: MUST be justified in terms of principles (especially I and II).

## Development Workflow

- All changes MUST comply with the five Core Principles.
- Principle compliance MUST be evaluated at every design gate (plan review, spec review,
  code review).
- Business logic tests MUST NOT require infrastructure (database, network, filesystem).
- Principle violations MUST be documented with justification and approved before merging.
- Observability (logging, metrics) MUST be added for all webhook processing paths.

## Governance

- This Constitution supersedes all other development practices.
- Amendments require:
  1. A documented rationale explaining the change.
  2. Approval by the project maintainer(s).
  3. A migration plan for any in-flight work affected by the change.
- Versioning follows Semantic Versioning (MAJOR.MINOR.PATCH):
  - MAJOR: Backward-incompatible principle removals or redefinitions.
  - MINOR: New principle or materially expanded guidance.
  - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
- All PRs and reviews MUST verify compliance with the Constitution.
- Complexity MUST be justified against principles — especially I (simplicity) and IV
  (modularity).

**Version**: 1.0.0 | **Ratified**: 2026-05-22 | **Last Amended**: 2026-05-22
