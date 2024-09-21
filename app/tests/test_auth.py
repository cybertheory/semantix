import pytest
from auth import verify_password, get_password_hash, create_access_token
from datetime import timedelta

def test_password_hashing():
    password = "testpassword"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data, expires_delta=timedelta(minutes=15))
    assert isinstance(token, str)
    assert len(token) > 0
