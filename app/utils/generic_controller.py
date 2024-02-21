from sqlalchemy import String, and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.utils.base_model import AbstractBaseModel
from app.utils.exceptions import IntegrityValidationException, ObjectNotFoundException


class GenericController:
    def __init__(self, model: AbstractBaseModel) -> None:
        self.model: AbstractBaseModel = model

    def get(self, db_session: Session, obj_id: int) -> AbstractBaseModel:

        instance = db_session.get(self.model, obj_id)
        if not instance:
            raise ObjectNotFoundException(self.model.__name__, obj_id)
        return instance

    def get_all(
        self, db_session: Session, skip: int = 0, limit: int = 100, **kwargs
    ) -> list[AbstractBaseModel]:
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

        return db_session.scalars(query.offset(skip).limit(limit)).all()

    def delete(self, db_session: Session, id: int) -> None:
        instance = self.get(db_session, id)
        if not instance:
            raise ObjectNotFoundException(self.model.__name__, id)

        db_session.delete(instance)
        db_session.commit()

    def save(self, db_session: Session, obj: AbstractBaseModel) -> AbstractBaseModel:
        try:
            db_session.add(obj)
            db_session.commit()
            db_session.refresh(obj)
        except IntegrityError as exc:
            db_session.rollback()
            raise IntegrityValidationException(exc.args[0]) from exc
        return obj

    def update(self, db_session: Session, obj: AbstractBaseModel) -> AbstractBaseModel:
        instance = self.get(db_session, obj.id)
        if not instance:
            raise ObjectNotFoundException(self.model.__name__, obj.id)

        for key, value in obj.as_dict().items():
            setattr(instance, key, value)

        try:
            db_session.commit()
        except IntegrityError as exc:
            db_session.rollback()
            raise IntegrityValidationException(exc.args[0]) from exc

        db_session.refresh(instance)
        return instance
