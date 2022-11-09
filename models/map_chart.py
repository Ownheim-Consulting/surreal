from models.chart import Chart
from models.datasets import ViewingAreas, DatasetLevels, WeatherDatasets, EconomicDatasets

from sqlalchemy import Column, Integer, String, ForeignKey

class MapChart(Chart):
    __abstract__ = True

    legend_title = Column(String(256))
    dataset_name = Column(String(256)) # Eg. Avg. Sal or Avg. Temp
    viewing_area_name = Column(String(256)) # Eg. USA
    dataset_level = Column(String(256)) # Eg. County

    def __init__(self,
                 title: str,
                 subtitle: str,
                 type: str,
                 legend_title: str,
                 dataset_name: (WeatherDatasets or EconomicDatasets),
                 viewing_area_name: ViewingAreas,
                 dataset_level: DatasetLevels) -> None:
        super(Chart, self).__init__(title, subtitle, type)
        self.legend_title = legend_title
        self.dataset_name = dataset_name
        self.viewing_area_name = viewing_area_name
        self.dataset_level = dataset_level
