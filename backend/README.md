# ECHO Backend

FastAPI modular backend foundation for the ECHO MVP.

## Run locally

```bash
cd backend
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
docker compose up -d postgres
psql postgresql://echo:echo@localhost:55432/echo -f migrations/001_initial.sql
uvicorn app.main:app --reload
```

Health: `GET http://localhost:8000/health`
Swagger UI: `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`
OpenAPI JSON: `http://localhost:8000/openapi.json`

OAuth provider secrets are intentionally absent from the repository. Configure them in `.env` before enabling the provider exchange adapters.
