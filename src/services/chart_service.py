from src.models.chart import Chart
from src.models.choropleth_map import ChoroplethMap
from src.models.response_model import ResponseModel
import src.utils.google_cloud as GC

class ChartsResponse(ResponseModel):
    def __init__(self, id: int, type: str, title: str, subtitle: str, url: str) -> None:
        self.id = id
        self.type = type
        self.title = title
        self.subtitle = subtitle
        self.url = url

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "type": self.type,
            "url": self.url,
        }

    @classmethod
    def from_chart(cls, chart: Chart):
        return cls(chart.id, chart.type, chart.title, chart.subtitle, chart.chart_url())

def get_choropleth_map(dataset_name: str, viewing_area: str, dataset_level: str) -> ChoroplethMap:
    choropleth_map: ChoroplethMap = ChoroplethMap.query.filter_by(dataset_name = dataset_name)\
    .filter_by(viewing_area_name = viewing_area)\
    .filter_by(dataset_level = dataset_level).first()

    if choropleth_map:
        (choropleth_map.geo_data_uri, choropleth_map.z_data_uri) = GC.add_signed_url_if_missing(choropleth_map.geo_data_uri, choropleth_map.z_data_uri)
    return choropleth_map

def get_choropleth_map_by_id(choropleth_chart_id: int) -> ChoroplethMap:
    choropleth_map: ChoroplethMap = ChoroplethMap.query.filter_by(chart_id = choropleth_chart_id).first()
    return choropleth_map

def get_all_charts() -> list:
    charts = [ChartsResponse.from_chart(chart) for chart in Chart.query.all()]
    return charts

def get_chart_by_id(chart_id: int) -> Chart:
    chart: Chart = Chart.query.filter_by(chart_id = chart_id).first()
    return chart
