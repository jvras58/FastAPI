"""Security utilities for password hashing and JWT token management."""
from datetime import UTC, datetime, timedelta

from bcrypt import checkpw, gensalt, hashpw
from jose import jwt

from app.utils.settings import get_settings


def create_access_token(data: dict) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    current_time = datetime.now(UTC)
    expire = current_time + timedelta(
        minutes=get_settings().SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})
    to_encode.update({'nbf': current_time})
    to_encode.update({'iat': current_time})
    to_encode.update({'iss': 'FA-Backend'})

    encoded_jwt = jwt.encode(
        to_encode,
        get_settings().SECURITY_API_SECRET_KEY,
        algorithm=get_settings().SECURITY_ALGORITHM,
    )

    return encoded_jwt


def get_password_hash(password: str) -> str:
    """Generate a hashed password."""
    salt = gensalt()
    return hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    plain_password_encoded = plain_password.encode('utf-8')

    # Esta converção é necessária para que o bcrypt consiga comparar
    # as senhas quando a string vem do BD.
    hashed_password_bytes = hashed_password.encode('utf-8')

    return checkpw(plain_password_encoded, hashed_password_bytes)


def extract_username(jwt_token: str) -> str:
    """
    docstring
    """
    payload = jwt.decode(
        jwt_token,
        get_settings().SECURITY_API_SECRET_KEY,
        algorithms=[get_settings().SECURITY_ALGORITHM],
    )
    return payload.get('sub') or ''
