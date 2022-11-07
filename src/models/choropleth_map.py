from src.database import Base
from src.models.datasets import ViewingAreas, DatasetLevels, WeatherDatasets, EconomicDatasets, GeoDataFormat, ZDataFormat
from src.models.map_chart import MapChart

from sqlalchemy import Column, String, Integer, ForeignKey

class ChoroplethMap(MapChart):
    __tablename__ = 'choropleth_map'

    id = Column(Integer, ForeignKey("chart.id"), primary_key=True)
    geo_data_uri = Column(String(512))
    geo_data_format = Column(String(50)) # Eg. JSON, CSV
    z_data_uri = Column(String(512))
    z_data_format = Column(String(50)) # Eg. JSON, CSV

    __mapper_args__ = {
        "polymorphic_identity": "choropleth_map"
    }

    def __init__(self,
                 title: str,
                 subtitle: str,
                 type: str,
                 legend_title: str,
                 dataset_name: (WeatherDatasets or EconomicDatasets),
                 viewing_area_name: ViewingAreas,
                 dataset_level: DatasetLevels,
                 geo_data_uri: str,
                 geo_data_format: GeoDataFormat,
                 z_data_uri: str,
                 z_data_format: ZDataFormat) -> None:
        super(MapChart, self).__init__(title, subtitle, type, legend_title,\
                                       dataset_name, viewing_area_name, dataset_level)
        self.geo_data_uri = geo_data_uri
        self.geo_data_format = geo_data_format.value
        self.z_data_uri = z_data_uri
        self.z_data_format = z_data_format.value

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "legend_title": self.legend_title,
            "dataset_name": self.dataset_name,
            "viewing_area": self.viewing_area_name,
            "dataset_level": self.dataset_level,
            "geo_data_uri": self.geo_data_uri,
            "geo_data_format": self.geo_data_format,
            "z_data_uri": self.z_data_uri,
            "z_data_format": self.z_data_format,
        }

    def chart_url(self) -> str:
        return "/api/chart/choropleth-map/dataset/{}/viewing-area/{}/level/{}"\
            .format(self.dataset_name, self.viewing_area_name, self.dataset_level)
