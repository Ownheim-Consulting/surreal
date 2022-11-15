from abc import ABC, abstractmethod

from database import Base

from sqlalchemy.orm import Session

class BaseRepo(ABC):
    entity: Base = NotImplementedError
    db: Session = NotImplementedError

    def __init__(self, db: Session, entity: Base) -> None:
        self.db = db
        self.entity = entity

    @abstractmethod
    def get(self, id: any) -> entity:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def persist(self, entity) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity) -> None:
        raise NotImplementedError
