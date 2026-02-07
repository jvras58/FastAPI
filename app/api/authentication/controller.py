"""Authentication controller module."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.api.authentication.schemas import TokenData
from app.api.user.controller import UserController
from app.database.session import Session, get_session
from app.models.user import User
from app.utils.exceptions import (
    CredentialsValidationException,
    IncorrectCredentialException,
)
from app.utils.logging import get_logger
from app.utils.security import (
    create_access_token,
    extract_username,
    verify_password,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

SessionDep = Annotated[Session, Depends(get_session)]
OAuth2Token = Annotated[str, Depends(oauth2_scheme)]

user_controller = UserController()
logger = get_logger("authentication.controller")


def execute_user_login(db_session: SessionDep, username: str, password: str) -> dict:
    """Authenticate user and return JWT token."""
    logger.info("Authenticating username=%s", username)
    db_user = user_controller.get_user_by_username(db_session, username)

    if not db_user:
        logger.warning("Authentication failed: user not found username=%s", username)
        raise IncorrectCredentialException()

    if not verify_password(password, db_user.password):
        logger.warning("Authentication failed: invalid password username=%s", username)
        raise IncorrectCredentialException()

    token = create_access_token(data={"sub": db_user.username})
    logger.info("Authentication success username=%s", username)

    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(db_session: SessionDep, token: OAuth2Token) -> User:
    """Get current user from JWT token."""
    token_data = TokenData()
    try:
        username = extract_username(token)
        if not username:
            logger.warning("Token missing subject")
            raise CredentialsValidationException()

        token_data.username = username
    except JWTError as ex:
        logger.warning("Token decode failed")
        raise CredentialsValidationException() from ex

    db_user = user_controller.get_user_by_username(db_session, token_data.username)

    if db_user is None:
        logger.warning("Token subject not found username=%s", token_data.username)
        raise CredentialsValidationException()
    return db_user
