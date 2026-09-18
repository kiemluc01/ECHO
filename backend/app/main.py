from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.routes import account, auth, health, inventory, players
from app.core.config import get_settings

settings = get_settings()

tags_metadata = [
	{"name": "health", "description": "Service liveness and readiness checks."},
	{"name": "auth", "description": "OAuth provider and token lifecycle endpoints."},
	{"name": "account", "description": "Authenticated account operations."},
	{"name": "players", "description": "Character profile operations."},
	{"name": "inventory", "description": "Inventory and wallet read APIs."},
]

app = FastAPI(
	title=settings.app_name,
	description="Platform API foundation for the ECHO persistent online RPG.",
	version="0.1.0",
	openapi_url="/openapi.json",
	docs_url="/docs",
	redoc_url="/redoc",
	openapi_tags=tags_metadata,
	contact={"name": "ECHO Backend Team"},
	license_info={"name": "Proprietary"},
)


def custom_openapi() -> dict:
	if app.openapi_schema:
		return app.openapi_schema

	schema = get_openapi(
		title=app.title,
		version=app.version,
		description=app.description,
		routes=app.routes,
		tags=tags_metadata,
	)
	schema["servers"] = [{"url": "/", "description": "Current environment"}]
	schema.setdefault("components", {}).setdefault("schemas", {}).update(
		{
			"ErrorBody": {
				"type": "object",
				"required": ["code", "message"],
				"properties": {
					"code": {"type": "string", "example": "AUTH_REQUIRED"},
					"message": {"type": "string", "example": "Authentication required"},
					"details": {"type": "object", "default": {}},
				},
			}
		}
	)
	app.openapi_schema = schema
	return app.openapi_schema


app.openapi = custom_openapi

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
app.include_router(account.router, prefix="/v1", tags=["account"])
app.include_router(players.router, prefix="/v1", tags=["players"])
app.include_router(inventory.router, prefix="/v1", tags=["inventory"])
