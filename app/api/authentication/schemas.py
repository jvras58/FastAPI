"""Authentication schemas."""
from pydantic import BaseModel


class AccessToken(BaseModel):
    """
    Represents a JWT token response.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Represents the logged user data within the JWT token (access_token).
    """

    username: str | None = None
