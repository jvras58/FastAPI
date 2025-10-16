"""Generic controller for CRUD operations."""
from typing import Generic, TypeVar

from sqlalchemy import String, and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.utils.base_model import AbstractBaseModel
from app.utils.exceptions import (
    IntegrityValidationException,
    ObjectNotFoundException,
)

T = TypeVar('T', bound=AbstractBaseModel)


class GenericController(Generic[T]):
    """Generic controller for CRUD operations."""

    def __init__(self, model: type[T]) -> None:
        """Initialize the controller with a specific model."""
        self.model: type[T] = model

    def get(self, db_session: Session, obj_id: int) -> T:
        """Get an object by its ID."""
        instance = db_session.get(self.model, obj_id)
        if not instance:
            raise ObjectNotFoundException(self.model.__name__, str(obj_id))
        return instance

    def get_all(
        self, db_session: Session, skip: int = 0, limit: int = 100, **kwargs
    ) -> list[T]:
        """Get all objects with optional filtering and pagination."""
        query = select(self.model)
        if kwargs:
            criteria_and = []
            for key, value in kwargs.items():
                field = getattr(self.model, key)
                if isinstance(field.property.columns[0].type, String):
                    criteria_and.append(field.ilike(f'%{value}%'))
                else:
                    criteria_and.append(field == value)

            query = query.filter(and_(*criteria_and))

        return list(db_session.scalars(query.offset(skip).limit(limit)).all())

    def delete(self, db_session: Session, obj_id: int) -> None:
        """Delete an object by its ID."""
        instance = self.get(db_session, obj_id)
        if not instance:
            raise ObjectNotFoundException(self.model.__name__, str(obj_id))

        db_session.delete(instance)
        db_session.commit()

    def save(self, db_session: Session, obj: T) -> T:
        """Save a new object to the database."""
        try:
            db_session.add(obj)
            db_session.commit()
            db_session.refresh(obj)
        except IntegrityError as exc:
            db_session.rollback()
            raise IntegrityValidationException(exc.args[0]) from exc
        return obj

    def update(self, db_session: Session, obj: T) -> T:
        """Update an existing object in the database."""
        obj_id = getattr(obj, 'id', None)
        if obj_id is None:
            raise ValueError(
                "Object must have an 'id' attribute for update operations"
            )

        instance = self.get(db_session, obj_id)
        if not instance:
            raise ObjectNotFoundException(self.model.__name__, str(obj_id))

        for key, value in obj.as_dict().items():
            setattr(instance, key, value)

        try:
            db_session.commit()
        except IntegrityError as exc:
            db_session.rollback()
            raise IntegrityValidationException(exc.args[0]) from exc

        db_session.refresh(instance)
        return instance
