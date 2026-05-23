from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.ports.user_repository import (
    UserData,
    UserRecord,
    UserRepository,
)
from src.infrastructure.database.models.user import UserModel


class PostgresUserRepository(UserRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_record(model: UserModel) -> UserRecord:
        return UserRecord(
            id=model.id,
            github_id=model.github_id,
            username=model.username,
            display_name=model.display_name,
            avatar_url=model.avatar_url,
            encrypted_token=model.encrypted_token,
            token_nonce=model.token_nonce,
            github_connected_at=model.github_connected_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def create(self, data: UserData) -> UserRecord:
        model = UserModel(
            github_id=data.github_id,
            username=data.username,
            display_name=data.display_name,
            avatar_url=data.avatar_url,
            encrypted_token=data.encrypted_token,
            token_nonce=data.token_nonce,
            github_connected_at=data.github_connected_at,
        )
        self._session.add(model)
        await self._session.flush()
        return self._to_record(model)

    async def get_by_github_id(self, github_id: int) -> UserRecord | None:
        stmt = select(UserModel).where(UserModel.github_id == github_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_record(model) if model else None

    async def get_by_username(self, username: str) -> UserRecord | None:
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_record(model) if model else None

    async def get_by_id(self, user_id: UUID) -> UserRecord | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_record(model) if model else None

    async def update_token(
        self, user_id: UUID, encrypted_token: bytes, token_nonce: bytes
    ) -> None:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(
                encrypted_token=encrypted_token,
                token_nonce=token_nonce,
            )
        )
        await self._session.execute(stmt)

    async def delete(self, user_id: UUID) -> None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
