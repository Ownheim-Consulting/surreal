from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from types import NotImplementedType
from typing import Any, Generic, TypeVar

T = TypeVar('T')

@dataclass
class BaseRepo(ABC, Generic[T]):
    db: Any = NotImplementedError
    model: T = NotImplementedType

    @abstractmethod
    def get(self, id: Any) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def get_by_params(self, **params: dict[str, Any]) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_all_by_params(self, **params: dict[str, Any]) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def persist(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def persist_all(self, entities: Sequence[T]) -> None:
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
