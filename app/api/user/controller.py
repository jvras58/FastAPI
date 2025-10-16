"""Controller for user-related operations."""
from sqlalchemy import select

from app.database.session import Session
from app.models.user import User
from app.utils.base_model import AbstractBaseModel
from app.utils.generic_controller import GenericController
from app.utils.security import get_password_hash


class UserController(GenericController):
    """Controller for user-related operations."""

    def __init__(self) -> None:
        super().__init__(User)

    def get_user_by_username(
        self, db_session: Session, username: str
    ) -> User | None:
        """Get a user by their username."""
        return db_session.scalar(select(User).where(User.username == username))

    def save(self, db_session: Session, obj: User) -> AbstractBaseModel:
        """Save a new user to the database with hashed password."""
        obj.password = get_password_hash(obj.password)
        return super().save(db_session, obj)

    def update(self, db_session: Session, obj: User) -> AbstractBaseModel:
        """Update an existing user in the database with hashed password."""
        obj.password = get_password_hash(obj.password)
        return super().update(db_session, obj)
