from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserData:
    github_id: int
    username: str
    display_name: str | None
    avatar_url: str | None
    encrypted_token: bytes
    token_nonce: bytes
    github_connected_at: datetime


@dataclass
class UserRecord(UserData):
    id: UUID
    created_at: datetime
    updated_at: datetime


class UserRepository(ABC):

    @abstractmethod
    async def create(self, data: UserData) -> UserRecord:
        ...

    @abstractmethod
    async def get_by_github_id(self, github_id: int) -> UserRecord | None:
        ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserRecord | None:
        ...

    @abstractmethod
    async def update_token(
        self, user_id: UUID, encrypted_token: bytes, token_nonce: bytes
    ) -> None:
        ...

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        ...
