from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
from pwdlib import PasswordHash

from fastapi_learning_project.core.config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hashes a password using the recommended hashing algorithm (Argon2id).
    
    Args:
        password: The plain text password to be hashed.
        
    Returns:
        The hashed password string.
    """
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a stored hash using constant-time comparison.
    
    Args:
        plain_password: The plain text password to verify.
        hashed_password: The stored hash to compare against.
        
    Returns:
        True if the password matches the hash, False otherwise.
    """
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """
    Creates a signed JWT access token with an expiration claim (exp).
    
    Args:
        data: Payload claims to include inside the token.
        expires_delta: Optional custom lifetime duration.
        
    Returns:
        Encoded and signed JWT string.
    """
    to_encode = data.copy()
    
    now = datetime.now(timezone.utc)
    if expires_delta is not None:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    
    encoded_jwt: str = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decodes and validates a JWT access token against the configured secret and algorithm.
    
    Args:
        token: Raw JWT token string received from client.
        
    Returns:
        The decoded payload dictionary.
        
    Raises:
        jwt.PyJWTError: If signature verification fails, token has expired, or claims are malformed.
    """
    payload: dict[str, Any] = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
    return payload