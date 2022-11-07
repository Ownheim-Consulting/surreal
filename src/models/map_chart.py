from src.models.chart import Chart

from sqlalchemy import Column, Integer, String, ForeignKey

class MapChart(Chart):
    __abstract__ = True

    legend_title = Column(String(256))
    dataset_name = Column(String(256)) # Eg. Avg. Sal or Avg. Temp
    viewing_area_name = Column(String(256)) # Eg. USA
    dataset_level = Column(String(256)) # Eg. County
