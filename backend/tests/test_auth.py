import pytest
from datetime import datetime, timedelta
from uuid import UUID

from jose import jwt

from backend.src.auth import create_access_token, get_current_user, ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException


def test_create_access_token():
    test_data = {"sub": "testuser", "user_id": UUID("12345678-1234-5678-1234-567812345678")}
    token = create_access_token(test_data)
    assert isinstance(token, str)

    # Decode and check payload
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_payload["sub"] == test_data["sub"]
    assert UUID(decoded_payload["user_id"]) == test_data["user_id"]
    assert "exp" in decoded_payload


def test_get_current_user_valid_token():
    test_user_id = UUID("12345678-1234-5678-1234-567812345678")
    test_data = {"sub": "testuser", "user_id": test_user_id}
    token = create_access_token(test_data)
    current_user = get_current_user(token)
    assert current_user["username"] == "testuser"
    assert current_user["user_id"] == test_user_id


def test_get_current_user_invalid_token():
    with pytest.raises(HTTPException) as exc_info:
        get_current_user("invalid_token")
    assert exc_info.value.status_code == 401


def test_get_current_user_expired_token():
    test_data = {"sub": "testuser", "user_id": UUID("12345678-1234-5678-1234-567812345678")}
    # Create an expired token by setting expires_minutes to a negative value
    expired_token = create_access_token(test_data, expires_minutes=-1)
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(expired_token)
    assert exc_info.value.status_code == 401


def test_get_current_user_no_sub_or_user_id_in_payload():
    # Token with missing 'sub'
    token_missing_sub = jwt.encode({"user_id": str(UUID("12345678-1234-5678-1234-567812345678")), "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token_missing_sub)
    assert exc_info.value.status_code == 401

    # Token with missing 'user_id'
    token_missing_user_id = jwt.encode({"sub": "testuser", "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token_missing_user_id)
    assert exc_info.value.status_code == 401
