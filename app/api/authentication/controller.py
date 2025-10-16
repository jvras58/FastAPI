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
from app.utils.security import (
    create_access_token,
    extract_username,
    verify_password,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

SessionDep = Annotated[Session, Depends(get_session)]
OAuth2Token = Annotated[str, Depends(oauth2_scheme)]

user_controller = UserController()


def execute_user_login(
    db_session: SessionDep, username: str, password: str
) -> dict:
    """Authenticate user and return JWT token."""
    db_user = user_controller.get_user_by_username(db_session, username)

    if not db_user:
        raise IncorrectCredentialException()

    if not verify_password(password, db_user.password):
        raise IncorrectCredentialException()

    token = create_access_token(data={'sub': db_user.username})

    return {'access_token': token, 'token_type': 'bearer'}


async def get_current_user(db_session: SessionDep, token: OAuth2Token) -> User:
    """Get current user from JWT token."""
    token_data = TokenData()
    try:
        username = extract_username(token)
        if not username:
            raise CredentialsValidationException()

        token_data.username = username
    except JWTError as ex:
        raise CredentialsValidationException() from ex

    db_user = user_controller.get_user_by_username(
        db_session, token_data.username
    )

    if db_user is None:
        raise CredentialsValidationException()
    return db_user
