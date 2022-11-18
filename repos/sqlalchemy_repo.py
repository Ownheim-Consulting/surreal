from dataclasses import dataclass
from typing import TypeVar

from database import Base
from repos.base_repo import BaseRepo

from sqlalchemy.orm import Session

T = TypeVar('T', bound=Base)

@dataclass
class SqlAlchemyRepo(BaseRepo[T]):
    db: Session
    model: T

    def get(self, id: any) -> T:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> list:
        return self.db.query(self.model).all()

    def get_by_params(self, **params: dict) -> T:
        query = self.db.query(self.model)
        for key, value in params.items():
            query.filter(key == value)
        return query.first()

    def get_all_by_params(self, **parms: dict) -> T:
        query = self.db.query(self.model)
        for key, value in params.items():
            query.filter(key == value)
        return query.all()

    def persist(self, entity: T) -> None:
        self.db.add(entity)

    def update(self, entity: T) -> None:
        self.db.update()

    def delete(self, entity: T) -> None:
        self.db.delete(entity)

    def begin(self) -> None:
        self.db.begin()

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
