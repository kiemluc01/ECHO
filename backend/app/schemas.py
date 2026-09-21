import unicodedata
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


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


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class CharacterCreate(BaseModel):
    """`name` accepts any Unicode letter, so Vietnamese names work; see `_normalise_name`."""

    name: str = Field(min_length=3, max_length=64)
    gender: Gender

    @field_validator("name")
    @classmethod
    def _normalise_name(cls, value: str) -> str:
        # NFC first: "Lê" typed as e + combining acute must not become a second, distinct name
        # from the precomposed spelling, since the column is UNIQUE.
        value = unicodedata.normalize("NFC", value).strip()
        if any(unicodedata.category(character) in {"Cc", "Cf", "Zl", "Zp"} for character in value):
            raise ValueError("name contains control or invisible characters")
        if "  " in value:
            raise ValueError("name contains repeated spaces")
        if not all(character.isalnum() or character in " _-" for character in value):
            raise ValueError("name may only contain letters, digits, spaces, _ or -")
        if not 3 <= len(value) <= 64:
            raise ValueError("name must be 3-64 characters after trimming")
        return value


class CharacterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    gender: str
    level: int
    xp: int
    status: str


class QuestResponse(BaseModel):
    """A quest from the catalog together with this character's progress on it."""

    model_config = ConfigDict(from_attributes=True)

    code: str
    title: str
    summary: str
    objective: str
    required_progress: int
    reward_xp: int
    state: str
    progress: int


class QuestProgressUpdate(BaseModel):
    progress: int = Field(ge=0)


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


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    display_name: str | None = Field(default=None, min_length=2, max_length=64)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class RefreshRequest(BaseModel):
    refresh_token: str
