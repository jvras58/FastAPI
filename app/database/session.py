from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.utils.settings import get_settings

engine = create_engine(get_settings().DB_URL)


def get_session():
    with Session(engine) as session:
        yield session
