from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class GitHubUserInfo:
    github_id: int
    username: str
    display_name: str | None
    avatar_url: str | None


@dataclass
class TokenExchangeResult:
    access_token: str
    user: GitHubUserInfo


class GitHubOAuthPort(ABC):

    @abstractmethod
    def get_authorization_url(self, state: str) -> str:
        ...

    @abstractmethod
    async def exchange_code(self, code: str) -> TokenExchangeResult:
        ...
