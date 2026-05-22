# Feature Specification: GitHub Plant Gamification

**Feature Branch**: `001-github-plant`

**Created**: 2026-05-22

**Status**: Draft

**Input**: User description: "Interactive web app that gamifies a user's GitHub contribution history. Features: 1) GitHub auth integration, 2) Plant selection (Cactus, Bonsai, Cannabis, Fruit), 3) Watering via commits, 4) Growth stages (seed, sprout, young, mature, bloomed), 5) Interactive dashboard with animations"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Connect GitHub Account (Priority: P1)

A user visits the app for the first time, authenticates with their GitHub account via OAuth, and grants permission for the app to read their public contribution data.

**Why this priority**: Without authentication, there is no GitHub data and no personalized experience — this is the foundational user story.

**Independent Test**: New visitor clicks "Connect GitHub", completes OAuth flow, is redirected back to the app, and sees their GitHub username displayed in the dashboard header.

**Acceptance Scenarios**:

1. **Given** a new visitor who has not connected GitHub, **When** they click "Connect with GitHub", **Then** they are redirected to GitHub's OAuth authorization page.
2. **Given** the user has authorized the app on GitHub, **When** GitHub redirects back to the app, **Then** the app displays a welcome message and prompts for plant selection.
3. **Given** the user denies authorization on GitHub, **When** they return to the app, **Then** a friendly error message is shown with a "Try Again" button.

---

### User Story 2 - Select a Plant (Priority: P1)

After connecting GitHub, the user chooses a plant type from the available options (Cactus, Bonsai, Cannabis, Fruit Plant) to represent their growth journey.

**Why this priority**: The plant is the core visual metaphor — the experience cannot start without this choice.

**Independent Test**: After GitHub auth, user is shown 4 plant cards, selects one, and is taken to the dashboard where their plant appears as a seed.

**Acceptance Scenarios**:

1. **Given** the user has just connected GitHub, **When** they see the plant selection screen, **Then** they are presented with at least 4 distinct plant options, each with a preview image and name.
2. **Given** the user selects a plant type, **When** they confirm their choice, **Then** the dashboard loads showing their plant in the "seed" stage.
3. **Given** the user is on the plant selection screen, **When** they hover over a plant option, **Then** a tooltip shows the plant's name and a short description.

---

### User Story 3 - Receive Water Drops from Commits (Priority: P2)

As commits are detected in the user's GitHub account (both historical on first connection and new ones via webhook), each one translates into a water drop that accumulates toward the next growth stage.

**Why this priority**: The drip mechanic is the core loop — without drops the plant never grows, making the experience static.

**Independent Test**: User connects a GitHub account with at least 20 public commits. The plant receives drops equal to the commit count and progresses through at least one growth stage on the dashboard.

**Acceptance Scenarios**:

1. **Given** the user has connected their GitHub account, **When** the initial contribution history is imported, **Then** each detected commit from the past year generates a water drop, and the plant advances stages accordingly (capped at bloomed).
2. **Given** a user with an active connection, **When** a new commit is pushed to any public repository, **Then** within 60 seconds the plant receives an additional drop and an animation plays.
3. **Given** the user has accumulated enough drops, **When** the threshold for the next growth stage is met, **Then** the plant transforms to the next stage with a growth animation.

---

### User Story 4 - View Dashboard (Priority: P2)

The user visits the dashboard to see their plant's current state, total drops, drop history, and growth progress.

**Why this priority**: The dashboard is the primary interface — without it the user has no way to see their progress.

**Independent Test**: Authenticated user navigates to the dashboard and sees the plant visual, a numeric drop counter, a progress bar toward the next stage, and a chronological list of recent drops.

**Acceptance Scenarios**:

1. **Given** an authenticated user with an active plant, **When** they visit the dashboard, **Then** they see the plant rendered at its current growth stage.
2. **Given** the user has accumulated drops, **When** viewing the dashboard, **Then** a counter shows total drops received.
3. **Given** the user has drop history, **When** scrolling the dashboard, **Then** a chronological list of recent drops (date, source repository) is displayed.
4. **Given** the plant has not yet reached the final stage, **When** viewing the dashboard, **Then** a progress indicator shows drops toward the next stage.

---

### User Story 5 - Watering Animations (Priority: P3)

When a new drop is detected (via webhook), the dashboard shows a brief visual animation of water falling onto the plant.

**Why this priority**: Animations create the gamified experience and delight users, but the core functionality works without them.

**Independent Test**: User has dashboard open. A new commit is pushed to their GitHub. Within seconds, a water drop animation plays on the plant and the counter increments.

**Acceptance Scenarios**:

1. **Given** the user is viewing the dashboard, **When** a new drop is received, **Then** a single water droplet animation falls from the top of the plant area and is absorbed.
2. **Given** the user is viewing the dashboard, **When** the plant transitions to a new growth stage, **Then** a distinct transformation animation plays (e.g., glow, size change, sparkle).
3. **Given** the dashboard is open and multiple drops arrive in quick succession, **When** each is processed, **Then** animations queue and play sequentially without overlapping.

### Edge Cases

- What happens when the user has zero public commits? → Plant remains seed, informative message: "Start committing to grow your plant!"
- What happens when the plant reaches bloomed (final stage)? → Drops still count and are displayed, but no further visual change; a "Max Level" badge appears.
- How does the system handle GitHub API rate limits? → Drops from historical import are rate-limited; webhooks are the primary real-time channel; a status indicator shows "Sync paused — GitHub rate limit reached" if needed.
- What happens when the user disconnects their GitHub account? → Plant freezes at current stage; data is preserved for 30 days before deletion.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to authenticate via GitHub OAuth 2.0.
- **FR-002**: System MUST request only the `read:user` and `public_repo` OAuth scopes.
- **FR-003**: System MUST fetch the user's public contribution history from GitHub upon first connection.
- **FR-004**: System MUST display a plant selection screen after successful GitHub authentication.
- **FR-005**: System MUST support at least 4 plant types: Cactus, Bonsai, Cannabis, and Fruit Plant.
- **FR-006**: Each plant type MUST have 5 distinct growth stages: seed, sprout, young, mature, bloomed.
- **FR-007**: System MUST map each detected GitHub commit to one water drop for the user's plant.
- **FR-008**: System MUST apply drops from the initial historical import immediately upon calculation.
- **FR-009**: System MUST process new commits via GitHub webhooks and award drops within 60 seconds.
- **FR-010**: System MUST advance the plant's growth stage when the accumulated drop threshold is met.
- **FR-011**: Growth stage thresholds MUST increase per stage: seed→sprout (5 drops), sprout→young (15 drops), young→mature (30 drops), mature→bloomed (50 drops).
- **FR-012**: System MUST display the plant at its current growth stage on the dashboard.
- **FR-013**: System MUST show a total drop counter on the dashboard.
- **FR-014**: System MUST show a chronological list of recent drops with timestamps and source repository.
- **FR-015**: System MUST play a watering animation when a new drop is detected in real-time.
- **FR-016**: System MUST play a stage transition animation when the plant grows to the next stage.
- **FR-017**: System MUST NOT store GitHub tokens in plaintext — encryption at rest is REQUIRED.
- **FR-018**: System MUST allow the user to disconnect their GitHub account, freezing the plant at its current stage.

### Key Entities

- **User**: Represents a human user linked to a GitHub account. Attributes: GitHub ID, username, display name, avatar URL, encrypted access token, connection status.
- **Plant**: The user's chosen plant with its growth state. Attributes: type, current growth stage, total drops accumulated, drops in current stage, user ID.
- **PlantType**: A template defining a species of plant. Attributes: name, description, preview image, growth stage definitions (visual assets per stage, thresholds).
- **Drop**: An event record of a detected contribution. Attributes: type (commit/pull_request), source repository, timestamp, GitHub event ID, plant ID.
- **GrowthStage**: A named stage in a plant's lifecycle. Attributes: name, ordinal (1-5), drop threshold required, visual asset reference.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete GitHub OAuth flow and reach the plant selection screen in under 30 seconds.
- **SC-002**: Each plant type is visually distinct across all 5 growth stages (verified by user test: 9/10 users can identify which plant they selected).
- **SC-003**: New GitHub commits are reflected as water drops on the dashboard within 60 seconds of the push event.
- **SC-004**: 100% of stored GitHub tokens are encrypted at rest (verified by audit).
- **SC-005**: A user with 50+ public commits in the past year can advance their plant to bloomed stage on first load.
- **SC-006**: Drop counter accuracy matches actual commit count within 1% margin (verified by end-to-end test against GitHub API).

## Assumptions

- The user has a GitHub account with at least one public repository.
- Growth thresholds are balanced for casual developers (~50 commits/year). Advanced users will reach bloomed quickly on first import then sustain with ongoing commits.
- Only public repository contributions are tracked by default. Private repo tracking is out of scope for v1.
- Webhook delivery is the primary real-time mechanism; a daily polling fallback ensures consistency.
- The app is single-user (personal dashboard). Multi-tenancy is future scope.
- Growth stages use SVG-based visuals for resolution independence and animation support.
- Historical import covers the past 12 months of contributions.
- Users access the app via a modern web browser (last 2 major versions of Chrome, Firefox, Safari, Edge).
