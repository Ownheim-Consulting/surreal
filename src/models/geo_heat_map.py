from enum import Enum
import uuid

from src.database import Base

from sqlalchemy import Column, Float, String, Integer

class GeoHeatMap(Base):
    __tablename__ = 'geo_heat_maps'

    id = Column('geo_heat_map_id', Integer, primary_key=True, autoincrement=True)
    title = Column(String(256))
    dataset_name = Column(String(256)) # Eg. Avg. Sal
    viewing_area_name = Column(String(256)) # Eg. USA
    dataset_level = Column(String(256)) # Eg. County
    geojson_uri = Column(String(512))
    zjson_uri = Column(String(512))

    def __init__(self, title, dataset_name: str, viewing_area_name: str, dataset_level: str, json_uri, zjson_uri):
        self.title = title
        self.dataset_name = dataset_name
        self.viewing_area_name = viewing_area_name
        self.dataset_level = dataset_level
        self.geojson_uri = json_uri
        self.zjson_uri = zjson_uri

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "dataset_name": self.dataset_name,
            "viewing_area": self.viewing_area_name,
            "dataset_level": self.dataset_level,
            "geojson_uri": self.geojson_uri,
            "zjson_uri": self.zjson_uri,
        }
