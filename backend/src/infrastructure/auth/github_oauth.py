import httpx
from authlib.integrations.httpx_client import AsyncOAuth2Client

from src.core.config.settings import settings
from src.core.ports.github_oauth import (
    GitHubOAuthPort,
    GitHubUserInfo,
    TokenExchangeResult,
)


class GitHubOAuthService(GitHubOAuthPort):

    AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
    TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_API = "https://api.github.com/user"

    def get_authorization_url(self, state: str) -> str:
        params = {
            "client_id": settings.github_client_id,
            "redirect_uri": "http://localhost:8000/api/auth/github/callback",
            "scope": "read:user,public_repo",
            "state": state,
        }
        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.AUTHORIZE_URL}?{query}"

    async def exchange_code(self, code: str) -> TokenExchangeResult:
        async with AsyncOAuth2Client(
            client_id=settings.github_client_id,
            client_secret=settings.github_client_secret,
        ) as client:
            token = await client.fetch_token(
                self.TOKEN_URL,
                code=code,
                redirect_uri="http://localhost:8000/api/auth/github/callback",
            )
            access_token = token.get("access_token", "")

        async with httpx.AsyncClient() as http:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github.v3+json",
            }
            resp = await http.get(self.USER_API, headers=headers)
            resp.raise_for_status()
            data = resp.json()

        user = GitHubUserInfo(
            github_id=data["id"],
            username=data["login"],
            display_name=data.get("name"),
            avatar_url=data.get("avatar_url"),
        )
        return TokenExchangeResult(access_token=access_token, user=user)
