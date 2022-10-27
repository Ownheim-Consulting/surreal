from src.database import Base
from src.models.datasets import ViewingAreas, DatasetLevels, WeatherDatasets, EconomicDatasets, GeoDataFormat, ZDataFormat

from sqlalchemy import Column, Float, String, Integer

class ChoroplethMap(Base):
    __tablename__ = 'choropleth_maps'

    id = Column('choropleth_map_id', Integer, primary_key=True, autoincrement=True)
    title = Column(String(256))
    legend_title = Column(String(256))
    dataset_name = Column(String(256)) # Eg. Avg. Sal or Avg. Temp
    viewing_area_name = Column(String(256)) # Eg. USA
    dataset_level = Column(String(256)) # Eg. County
    geo_data_uri = Column(String(512))
    geo_data_format = Column(String(50)) # Eg. JSON, CSV
    z_data_uri = Column(String(512))
    z_data_format = Column(String(50)) # Eg. JSON, CSV

    def __init__(self, title: str, dataset_name: (WeatherDatasets or EconomicDatasets),
                 viewing_area_name: ViewingAreas, dataset_level: DatasetLevels,
                 geo_data_uri: str, geo_data_format: GeoDataFormat,
                 z_data_uri: str, z_data_format: ZDataFormat):
        self.title = title
        self.dataset_name = dataset_name.value
        self.viewing_area_name = viewing_area_name.value
        self.dataset_level = dataset_level.value
        self.geo_data_uri = geo_data_uri
        self.geo_data_format = geo_data_format.value
        self.z_data_uri = z_data_uri
        self.z_data_format = z_data_format.value

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "legend_title": self.legend_title,
            "dataset_name": self.dataset_name,
            "viewing_area": self.viewing_area_name,
            "dataset_level": self.dataset_level,
            "geo_data_uri": self.geo_data_uri,
            "geo_data_format": self.geo_data_format,
            "z_data_uri": self.z_data_uri,
            "z_data_format": self.z_data_format,
        }
