from database import Base
from models.enum.datasets import ViewingAreas, DatasetLevels, WeatherDatasets, EconomicDatasets, GeoDataFormat, ZDataFormat
from models.database.map_chart import MapChart
from models.http.response_model import ResponseModel
import repos.external.google_cloud as GC

from sqlalchemy import Column, ForeignKey, Integer, String, event
from sqlalchemy.orm import QueryContext

class ChoroplethMap(MapChart):
    __tablename__ = 'choropleth_map'

    id = Column(Integer, ForeignKey('chart.id'), primary_key=True)
    geo_data_uri = Column(String(512))
    geo_data_format = Column(String(50)) # Eg. JSON, CSV
    z_data_uri = Column(String(512))
    z_data_format = Column(String(50)) # Eg. JSON, CSV

    __mapper_args__ = {
        'polymorphic_identity': 'choropleth_map'
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
        super().__init__(title, subtitle, type, legend_title,\
                                       dataset_name, viewing_area_name, dataset_level)
        self.geo_data_uri = geo_data_uri
        self.geo_data_format = geo_data_format.value
        self.z_data_uri = z_data_uri
        self.z_data_format = z_data_format.value

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'legend_title': self.legend_title,
            'dataset_name': self.dataset_name,
            'viewing_area': self.viewing_area_name,
            'dataset_level': self.dataset_level,
            'geo_data_uri': self.geo_data_uri,
            'geo_data_format': self.geo_data_format,
            'z_data_uri': self.z_data_uri,
            'z_data_format': self.z_data_format,
        }

@event.listens_for(ChoroplethMap, 'load', restore_load_context=True)
def on_load(instance: ChoroplethMap, context: QueryContext) -> None:
    if instance.geo_data_uri:
        instance.geo_data_uri = GC.add_signed_url_if_missing(instance.geo_data_uri)[0]
    if instance.z_data_uri:
        instance.z_data_uri = GC.add_signed_url_if_missing(instance.z_data_uri)[0]
