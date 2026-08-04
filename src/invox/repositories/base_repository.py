from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, entity: ModelType) -> ModelType:
        self.db_session.add(entity)
        self.db_session.commit()
        self.db_session.refresh(entity)
        return entity

    def clear_all(self, model) -> None:
        self.db_session.query(model).delete()
        self.db_session.commit()
