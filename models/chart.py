from abc import abstractmethod

from database import Base

from sqlalchemy import Column, String, Integer

class Chart(Base):
    __tablename__ = "chart"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256))
    subtitle = Column(String(256))
    type = Column(String(256))

    __mapper_args__ = {
        "polymorphic_identity": "chart",
        "polymorphic_on": type,
    }

    def __init__(self,
                 title: str,
                 subtitle: str,
                 type: str) -> None:
        self.title = title
        self.subtitle = subtitle
        self.type = type

    @abstractmethod
    def chart_url(self) -> str:
        raise NotImplementedError("Must implement chart_url(self) method in subclass of Chart")

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError("Must implement to_dict(self) method in sublass of Chart")
