from abc import ABC, abstractmethod

class ResponseModel(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError("Must implement to_dict(self) method in subclass of ResponseModel")
