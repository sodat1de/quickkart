import jwt, pytest
from quickkart_user import auth

def test_password_hash_roundtrip():
    plain = "s3cr3t"
    hashed = auth.hash_password(plain)
    assert auth.verify_password(plain, hashed)

def test_jwt_roundtrip():
    token = auth.create_access_token({"sub": "brandon@example.com"})
    payload = auth.decode_token(token)
    assert payload["sub"] == "brandon@example.com"
