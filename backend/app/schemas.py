from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ErrorBody(BaseModel):
    """Standard error payload documented in the OpenAPI schema."""

    code: str
    message: str
    details: dict = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    request_id: str = Field(..., alias="requestId", examples=["7e5d..."])
    error: ErrorBody

    model_config = ConfigDict(populate_by_name=True)


class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str | None
    provider: str
    status: str
    roles: list[str]


class CharacterCreate(BaseModel):
    name: str = Field(min_length=3, max_length=64, pattern=r"^[A-Za-z0-9 _-]+$")


class CharacterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    level: int
    xp: int
    status: str


class InventoryItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    item_template_code: str
    quantity: int
    status: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
