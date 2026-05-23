from datetime import datetime, timezone

from src.core.entities.drop import DropEventType
from src.core.services.drip_calculation import DripCalculationService


class TestDripCalculationService:

    def test_push_event_produces_drops(self):
        events = [
            {
                "delivery_id": "del-001",
                "event_type": "push",
                "committed_at": datetime.now(timezone.utc).isoformat(),
                "payload": {
                    "repository": {"full_name": "user/repo"},
                    "commits": [
                        {"id": "abc123", "timestamp": "2026-01-01T00:00:00Z"},
                        {"id": "def456", "timestamp": "2026-01-01T01:00:00Z"},
                    ],
                },
            }
        ]
        drops = DripCalculationService.calculate_drops(events)
        assert len(drops) == 2
        assert drops[0]["event_type"] == DropEventType.COMMIT
        assert drops[0]["source_repo"] == "user/repo"
        assert "del-001-commit-abc123" in drops[0]["github_event_id"]

    def test_merged_pr_produces_drop(self):
        events = [
            {
                "delivery_id": "del-002",
                "event_type": "pull_request",
                "committed_at": datetime.now(timezone.utc).isoformat(),
                "payload": {
                    "repository": {"full_name": "user/repo"},
                    "pull_request": {
                        "id": 42,
                        "merged": True,
                        "merged_at": "2026-02-01T00:00:00Z",
                    },
                },
            }
        ]
        drops = DripCalculationService.calculate_drops(events)
        assert len(drops) == 1
        assert drops[0]["event_type"] == DropEventType.PULL_REQUEST_MERGE
        assert "del-002-pr-42" in drops[0]["github_event_id"]

    def test_unmerged_pr_produces_no_drops(self):
        events = [
            {
                "delivery_id": "del-003",
                "event_type": "pull_request",
                "committed_at": datetime.now(timezone.utc).isoformat(),
                "payload": {
                    "repository": {"full_name": "user/repo"},
                    "pull_request": {
                        "id": 43,
                        "merged": False,
                    },
                },
            }
        ]
        drops = DripCalculationService.calculate_drops(events)
        assert len(drops) == 0

    def test_empty_push_produces_no_drops(self):
        events = [
            {
                "delivery_id": "del-004",
                "event_type": "push",
                "committed_at": datetime.now(timezone.utc).isoformat(),
                "payload": {
                    "repository": {"full_name": "user/repo"},
                    "commits": [],
                },
            }
        ]
        drops = DripCalculationService.calculate_drops(events)
        assert len(drops) == 0
