# ECHO Backend

FastAPI modular backend foundation for the ECHO MVP.

## Run locally

```bash
cd backend
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
docker compose up -d --build
psql postgresql://echo:echo@localhost:55432/echo -f migrations/001_initial.sql
psql postgresql://echo:echo@localhost:55432/echo -f migrations/002_local_auth.sql
uvicorn app.main:app --reload
```

Health: `GET http://localhost:8000/health`
Swagger UI: `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`
OpenAPI JSON: `http://localhost:8000/openapi.json`

OAuth provider secrets are intentionally absent from the repository. Configure them in `.env` before enabling the provider exchange adapters.

## OAuth login flow

1. Set `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `APPLE_CLIENT_ID`, and `APPLE_CLIENT_SECRET` in `.env`.
2. Register `http://localhost:8000/v1/auth/google/callback` and `http://localhost:8000/v1/auth/apple/callback` with the providers.
3. Unity opens the provider URL from `/v1/auth/{provider}/start`.
4. The server verifies the provider ID token, creates or finds the account, and redirects to `echo://auth/callback` with the issued tokens.
5. Unity stores the tokens locally and calls `/v1/me`.

### Email/password

Local accounts can also use:

```http
POST /v1/auth/register
Content-Type: application/json

{"email":"player@your-domain.com","password":"at-least-12-characters","display_name":"Player"}
```

Then login with `POST /v1/auth/login` using `email` and `password`. Passwords are stored as Argon2id hashes and never as plaintext.

For production, replace query-string token handoff with a one-time server-side authorization code and HTTPS universal/app links.
