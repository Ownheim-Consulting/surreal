from database import Base
from models.http.response_model import ResponseModel

from sqlalchemy import Column, String, Integer

class Chart(Base, ResponseModel):
    __tablename__ = 'chart'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256))
    subtitle = Column(String(256))
    type = Column(String(256))

    __mapper_args__ = {
        'polymorphic_identity': 'chart',
        'polymorphic_on': type,
    }

    def __init__(self,
                 title: str,
                 subtitle: str,
                 type: str) -> None:
        self.title = title
        self.subtitle = subtitle
        self.type = type
