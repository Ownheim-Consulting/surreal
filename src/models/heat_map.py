from sqlalchemy import Column, Integer, Float, String, LargeBinary
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class HeatMap(Base):
    __tablename__ = "heat_maps"

    id = Column('heat_map_id', Integer, primary_key = True)
    title = Column(String(256))
    data = Column(LargeBinary)
    lower_heat_boundary = Column(Float)
    upper_heat_boundary = Column(Float)
    lower_heat_color = Column(Integer)
    upper_heat_color = Column(Integer)

    def __init__(self, title: str, data: str,
                 lower_heat_boundary: float, upper_heat_boundary: float,
                 lower_heat_color: int, upper_heat_color: int):
        self.title = title
        self.data = data
        self.lower_heat_boundary = lower_heat_boundary
        self.upper_heat_boundary = upper_heat_boundary
        self.lower_heat_color = lower_heat_color
        self.upper_heat_color = upper_heat_color

    def to_dict(self):
        return {
            "chart_title": self.chart_title,
            "chart_data": self.chart_data,
            "lower_heat_boundary": self.lower_heat_boundary,
            "upper_heat_boundary": self.upper_heat_boundary,
            "lower_heat_color": self.lower_heat_color,
            "upper_heat_color": self.upper_heat_color,
        }
