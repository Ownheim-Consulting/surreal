from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, TypeVar

from sqlalchemy.orm.scoping import ScopedSession

from database import Base
from repos.database.base_repo import BaseRepo

from sqlalchemy.orm import Query, Session

T = TypeVar('T', bound=Base)

@dataclass
class SqlAlchemyRepo(BaseRepo[T]):
    db: Session | ScopedSession
    model: T

    def get(self, id: Any) -> T:
        return self.db.query(self.model).filter(self.model.id == id).one()

    def get_all(self) -> list[T]:
        return self.db.query(self.model).all()

    def get_by_params(self, **params: dict[str, Any]) -> T:
        query: Query[T] = self.db.query(self.model)
        for key, value in params.items():
            query.filter(key == value)
        return query.one()

    def get_all_by_params(self, **params: dict[str, Any]) -> list[T]:
        query: Query = self.db.query(self.model)
        for key, value in params.items():
            query.filter(key == value)
        return query.all()

    def persist(self, entity: T) -> None:
        self.db.add(entity)

    def persist_all(self, entities: Sequence[T]) -> None:
        self.db.add_all(entities)

    def update(self, _: T) -> None:
        raise NotImplementedError("SQLAlchemy does not have an update method. Changes are automatically persisted on commit.")

    def delete(self, entity: T) -> None:
        self.db.delete(entity)

    def begin(self) -> None:
        self.db.begin()

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
