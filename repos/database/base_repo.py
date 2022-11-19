from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar('T')

@dataclass
class BaseRepo(ABC, Generic[T]):
    db: any = NotImplementedError
    model: T = NotImplementedError

    @abstractmethod
    def get(self, id: any) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def get_by_params(self, **params: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all_by_params(self, **params: dict) -> T:
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

    @abstractmethod
    def begin(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
