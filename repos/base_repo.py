from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from database import Base

from sqlalchemy.orm import Session

T = TypeVar('T', bound=Base)

@dataclass
class BaseRepo(ABC, Generic[T]):
    db: Session = NotImplementedError
    model: T = NotImplementedError

    @abstractmethod
    def get(self, id: any) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def persist(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity: T) -> None:
        raise NotImplementedError
