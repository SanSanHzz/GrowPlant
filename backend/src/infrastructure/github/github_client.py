from datetime import UTC, datetime

import httpx

GITHUB_API = "https://api.github.com"


async def fetch_user_events(
    username: str, token: str, per_page: int = 100
) -> list[dict]:
    """Fetch public events for a GitHub user (last 90 days)."""
    url = f"{GITHUB_API}/users/{username}/events/public"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    all_events: list[dict] = []
    async with httpx.AsyncClient() as client:
        page = 1
        while True:
            resp = await client.get(
                url,
                headers=headers,
                params={"per_page": per_page, "page": page},
            )
            if resp.status_code != 200:
                break
            events = resp.json()
            if not events:
                break
            all_events.extend(events)
            page += 1

    return all_events


async def fetch_commit_history(
    username: str, token: str
) -> list[dict]:
    """Aggregate PushEvents into flat commit records for initial import."""
    events = await fetch_user_events(username, token)
    commits = []
    for event in events:
        if event.get("type") != "PushEvent":
            continue
        repo_full = event.get("repo", {}).get("name", "unknown/unknown")
        payload = event.get("payload", {})
        for c in payload.get("commits", []):
            commits.append(
                {
                    "event_type": "push",
                    "source_repo": repo_full,
                    "github_event_id": c.get("sha", ""),
                    "committed_at": _parse_iso(
                        c.get("timestamp")
                        or event.get("created_at")
                        or datetime.now(UTC).isoformat()
                    ),
                }
            )
    return commits


def _parse_iso(iso: str) -> datetime:
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return datetime.now(UTC)
