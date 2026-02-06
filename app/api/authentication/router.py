"""Authentication router module."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.authentication.controller import execute_user_login
from app.api.authentication.schemas import AccessToken
from app.database.session import Session, get_session
from app.utils.exceptions import IncorrectCredentialException
from app.utils.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

SessionDep = Annotated[Session, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=AccessToken)
def login_for_access_token(
    form_data: OAuth2Form, db_session: SessionDep
) -> dict:
    """Endpoint to obtain JWT token."""
    try:
        logger.info("Login attempt for username=%s", form_data.username)
        return execute_user_login(
            db_session, form_data.username, form_data.password
        )
    except IncorrectCredentialException as ex:
        logger.warning(
            "Login failed for username=%s: %s",
            form_data.username,
            ex.args[0],
        )
        raise HTTPException(status_code=400, detail=ex.args[0]) from ex
