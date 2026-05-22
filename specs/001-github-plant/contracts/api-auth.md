# Auth API Contracts

## GET /api/auth/github/login

Initiate GitHub OAuth flow — redirects user to GitHub authorization page.

**Response**: `302 Redirect` to `https://github.com/login/oauth/authorize?client_id=...&scope=read:user,public_repo`

---

## GET /api/auth/github/callback

GitHub OAuth callback — exchanges `code` for access token, creates/authenticates user.

**Query Parameters**:
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | string | yes | Temporary code from GitHub OAuth |
| `state` | string | yes | CSRF state token (must match session) |

**Response**: `200 OK`
```json
{
  "user": {
    "id": "uuid",
    "github_id": 12345,
    "username": "octocat",
    "display_name": "Octocat",
    "avatar_url": "https://avatars.githubusercontent.com/u/12345"
  },
  "session_token": "jwt-or-session-id"
}
```

**Error Responses**:
- `400` — Missing or invalid `code`/`state`
- `401` — GitHub authorization denied or token exchange failed

---

## GET /api/auth/status

Check authentication status — requires valid session token.

**Headers**: `Authorization: Bearer <session_token>`

**Response**: `200 OK`
```json
{
  "authenticated": true,
  "user": {
    "id": "uuid",
    "github_id": 12345,
    "username": "octocat",
    "display_name": "Octocat",
    "avatar_url": "https://avatars.githubusercontent.com/u/12345"
  }
}
```

**Error Responses**:
- `401` — Invalid or expired session token

---

## POST /api/auth/logout

Invalidate current session.

**Headers**: `Authorization: Bearer <session_token>`

**Response**: `200 OK`
```json
{
  "message": "Logged out successfully"
}
```
