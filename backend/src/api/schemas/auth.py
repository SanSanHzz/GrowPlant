from uuid import UUID

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: UUID
    github_id: int
    username: str
    display_name: str | None
    avatar_url: str | None

    model_config = {"from_attributes": True}


class LoginResponse(BaseModel):
    user: UserResponse
    session_token: str


class AuthStatusResponse(BaseModel):
    authenticated: bool
    user: UserResponse | None


class LogoutResponse(BaseModel):
    message: str
