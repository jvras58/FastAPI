from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.authentication.controller import execute_user_login
from app.api.authentication.schemas import AccessToken
from app.database.session import Session, get_session
from app.utils.exceptions import IncorrectCredentialException

router = APIRouter()

Session = Annotated[Session, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=AccessToken)
def login_for_access_token(form_data: OAuth2Form, db_session: Session):
    try:
        return execute_user_login(db_session, form_data.username, form_data.password)
    except IncorrectCredentialException as ex:
        raise HTTPException(status_code=400, detail=ex.args[0]) from ex
