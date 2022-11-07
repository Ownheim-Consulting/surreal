from src.database import Base

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
