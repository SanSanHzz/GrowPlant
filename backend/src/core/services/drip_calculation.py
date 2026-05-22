from src.core.entities.drop import DropEventType


class DripCalculationService:

    @staticmethod
    def calculate_drops(events: list[dict]) -> list[dict]:
        """Convert raw GitHub events into normalized drop records.

        Each event dict must have:
            - event_type: 'push' | 'pull_request'
            - payload: raw GitHub webhook payload
            - delivery_id: X-GitHub-Delivery header
            - committed_at: ISO datetime of the event timestamp

        Returns a list of dicts ready for DropRepository.create().
        """
        drops = []
        for event in events:
            if event["event_type"] == "push":
                commits = event.get("payload", {}).get("commits", [])
                repo_full = (
                    event.get("payload", {})
                    .get("repository", {})
                    .get("full_name", "unknown/unknown")
                )
                for commit in commits:
                    drops.append(
                        {
                            "plant_id": None,
                            "event_type": DropEventType.COMMIT,
                            "source_repo": repo_full,
                            "github_event_id": (
                                f"{event['delivery_id']}-commit-{commit.get('id', '')}"
                            ),
                            "committed_at": commit.get(
                                "timestamp", event["committed_at"]
                            ),
                        }
                    )

            elif event["event_type"] == "pull_request":
                pr = event.get("payload", {}).get("pull_request", {})
                if pr.get("merged", False):
                    repo_full = (
                        event.get("payload", {})
                        .get("repository", {})
                        .get("full_name", "unknown/unknown")
                    )
                    drops.append(
                        {
                            "plant_id": None,
                            "event_type": DropEventType.PULL_REQUEST_MERGE,
                            "source_repo": repo_full,
                            "github_event_id": (
                                f"{event['delivery_id']}-pr-{pr.get('id', '')}"
                            ),
                            "committed_at": pr.get(
                                "merged_at", event["committed_at"]
                            ),
                        }
                    )

        return drops
