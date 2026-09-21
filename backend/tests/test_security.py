from datetime import timedelta
from uuid import uuid4

import pytest

from app.core.config import Settings
from app.core.security import create_oauth_state, create_token, decode_access_token, decode_oauth_state, decode_refresh_token, hash_password, verify_password


def test_access_token_round_trip() -> None:
    settings = Settings(jwt_secret="test-secret")
    subject = uuid4()
    token = create_token(subject, ["player"], settings, "access", timedelta(minutes=5))
    payload = decode_access_token(token, settings)
    assert payload["sub"] == str(subject)
    assert payload["roles"] == ["player"]


def test_refresh_token_is_not_accepted_as_access_token() -> None:
    settings = Settings(jwt_secret="test-secret")
    token = create_token(uuid4(), ["player"], settings, "refresh", timedelta(days=1))
    with pytest.raises(ValueError):
        decode_access_token(token, settings)


def test_oauth_state_is_bound_to_provider() -> None:
    settings = Settings(jwt_secret="test-secret")
    state = create_oauth_state("google", settings)
    assert decode_oauth_state(state, settings, "google")["provider"] == "google"
    with pytest.raises(ValueError):
        decode_oauth_state(state, settings, "apple")


def test_refresh_token_round_trip() -> None:
    settings = Settings(jwt_secret="test-secret")
    token = create_token(uuid4(), ["player"], settings, "refresh", timedelta(days=1))
    assert decode_refresh_token(token, settings)["type"] == "refresh"


def test_password_hash_verification() -> None:
    password = "EchoTestPassword123"
    password_hash = hash_password(password)
    assert password_hash != password
    assert verify_password(password, password_hash)
    assert not verify_password("wrong-password", password_hash)
