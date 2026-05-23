# GitHub OAuth: Guía de Troubleshooting

## Arquitectura del flujo

```
Frontend (5173)                    Backend (8000)                GitHub
     │                                  │                        │
     │  click "Connect with GitHub"      │                        │
     │ ──GET /api/auth/github/login─────>│                        │
     │                                  │ 302 redirect            │
     │<─────── https://github.com/login/oauth/authorize? ─────────│
     │                                  │                        │
     │  User authorizes                                        │
     │                                  │  GET /callback?code=X  │
     │<─────────────────────────────────│<───────────────────────│
     │                                  │                        │
     │                                  │  POST /access_token    │
     │                                  │ ───────────────────────>│
     │                                  │  access_token          │
     │                                  │<───────────────────────│
     │                                  │                        │
     │  redirect /?token=JWT            │                        │
     │<─────────────────────────────────│                        │
     │                                  │                        │
     │  GET /api/auth/status            │                        │
     │ ────────────────────────────────>│                        │
     │  { authenticated: true }         │                        │
     │<────────────────────────────────│                        │
```

## Errores comunes y soluciones

### 1. `client_id=` vacío en la URL de GitHub

**Síntoma**: Al hacer login, la URL de autorización tiene `client_id=&redirect_uri=...`.

**Causa**: La variable de entorno `GITHUB_CLIENT_ID` no está configurada o no se carga correctamente.

**Solución**:
- Verificar que `.env` tenga `GITHUB_CLIENT_ID` y `GITHUB_CLIENT_SECRET` con valores válidos
- Verificar que `docker-compose.yml` tenga `env_file: .env` en el servicio backend
- Forzar rebuild con `docker compose up -d --build backend`

### 2. `redirect_uri` no URL-encoded

**Síntoma**: GitHub muestra "Authorizing will redirect to http://localhost:8000" (sin el path `/api/auth/github/callback`). Después de autorizar, el callback devuelve `422 Unprocessable Entity` o el navegador no recibe el `code`.

**Causa**: El `redirect_uri` en la URL de autorización no está URL-encoded. Código incorrecto:

```python
query = "&".join(f"{k}={v}" for k, v in params.items())  # ❌
```

**Solución**: Usar `urllib.parse.urlencode()`:

```python
from urllib.parse import urlencode
url = f"{AUTHORIZE_URL}?{urlencode(params)}"  # ✅
```

### 3. `redirect_uri` no coincide con el registro

**Síntoma**: GitHub redirige a la Homepage URL en vez del callback path. El backend no recibe el `code`.

**Causa**: El `redirect_uri` enviado en la URL de autorización no coincide EXACTAMENTE con el registrado en GitHub OAuth App.

**Solución**:
- Omite el `redirect_uri` de los params (GitHub usa el registrado por defecto):

```python
params = {
    "client_id": settings.github_client_id,
    "scope": "read:user,public_repo",
    "state": state,
}
```

- Asegurarse que la **Authorization callback URL** en GitHub sea exactamente igual (incluyendo protocolo, puerto y path):

```
http://localhost:8000/api/auth/github/callback
```

### 4. JWT `encode()` missing argument

**Síntoma**: Error `TypeError: encode() missing 1 required positional argument: 'key'` al crear el token de sesión.

**Causa**: La librería `joserfc.jwt.encode()` requiere 3 argumentos: `header`, `claims`, `key`.

```python
jwt_encode(claims, _jwk)  # ❌
```

**Solución**: Pasar también el header:

```python
jwt_encode({"alg": "HS256"}, claims, _jwk)  # ✅
```

### 5. Backend en bucle de recarga (hot-reload en Docker)

**Síntoma**: El backend se reinicia constantemente. Los logs muestran múltiples "Started server process [1]". El OAuth callback nunca se completa.

**Causa**: `uvicorn --reload` en Docker puede entrar en bucle por cómo el overlay filesystem reporta cambios.

**Solución**: Para desarrollo en Docker, usar:

```python
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]  # sin --reload
```

Y reiniciar manualmente con:
```bash
docker compose restart backend
```

### 6. Guard de Vue Router redirige al login

**Síntoma**: El OAuth funciona (se ve en logs), pero el frontend redirige de vuelta a `/` después de mostrar `/select-plant` brevemente.

**Causa**: El `beforeEach` guard usa el patrón viejo de Vue Router 3 con `next()`:

```javascript
router.beforeEach(async (to, _from, next) => {
  if (!authenticated) return next({ name: "login" });
  next();  // ❌ puede causar conflictos
});
```

**Solución**: Usar el patrón de Vue Router 4 sin `next()`:

```javascript
router.beforeEach(async (to) => {
  if (to.meta.requiresAuth) {
    const authenticated = await checkAuth();
    if (!authenticated) return { name: "login" };
  }
});
```

### 7. Sesión no persiste entre páginas

**Síntoma**: La autenticación funciona pero al recargar la página se pierde la sesión.

**Causa**: El token JWT se almacena solo en memoria o no se envía en las requests de la nueva página.

**Solución**: Guardar el token en `localStorage` y leerlo en cada request:

```typescript
function headers(): Record<string, string> {
  const token = localStorage.getItem("session_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}
```

## Configuración correcta de GitHub OAuth App

1. Ir a https://github.com/settings/developers → **OAuth Apps** → **New OAuth App**

2. Configurar:

| Campo | Valor |
|-------|-------|
| Application name | `GrowPlant` |
| Homepage URL | `http://localhost:8000` |
| Authorization callback URL | `http://localhost:8000/api/auth/github/callback` |

3. Una vez creado, generar un **Client Secret** (nunca compartir)

4. Agregar al `.env`:

```env
GITHUB_CLIENT_ID=Ov23li...
GITHUB_CLIENT_SECRET=1cebeb...
```

## Comandos útiles

```bash
# Verificar qué URL de autorización se genera
curl -s -o /dev/null -w "%{redirect_url}" http://localhost:8000/api/auth/github/login

# Probar callback con código inválido (esperar 401/302, no 500)
curl -v 'http://localhost:8000/api/auth/github/callback?code=test'

# Ver logs del backend
docker compose logs backend --tail 20

# Reconstruir y reiniciar
docker compose up -d --build backend

# Revocar autorización OAuth (para forzar re-autorización)
# Abrir en navegador:
# https://github.com/settings/connections/applications/<CLIENT_ID>
```
