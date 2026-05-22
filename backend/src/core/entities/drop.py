from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class DropEventType(StrEnum):
    COMMIT = "commit"
    PULL_REQUEST_MERGE = "pull_request_merge"


@dataclass
class Drop:
    id: UUID
    plant_id: UUID
    event_type: DropEventType
    source_repo: str
    github_event_id: str
    committed_at: object
    created_at: object
