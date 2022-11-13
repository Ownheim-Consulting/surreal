from models.chart import Chart
from models.choropleth_map import ChoroplethMap
from models.response_model import ResponseModel
import utils.google_cloud as GC

class ChartsResponse(ResponseModel):
    def __init__(self, id: int, type: str, title: str, subtitle: str) -> None:
        self.id = id
        self.type = type
        self.title = title
        self.subtitle = subtitle

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "type": self.type,
        }

    @classmethod
    def from_chart(cls, chart: Chart):
        return cls(chart.id, chart.type, chart.title, chart.subtitle)

def get_choropleth_map(dataset_name: str, viewing_area: str, dataset_level: str) -> ChoroplethMap:
    choropleth_map: ChoroplethMap = ChoroplethMap.query.filter_by(dataset_name = dataset_name)\
    .filter_by(viewing_area_name = viewing_area)\
    .filter_by(dataset_level = dataset_level).first()

    if not choropleth_map:
        raise ResourceNotFound("Could not find choropleth map for dataset: {}, viewing-area: {}, and dataset-level: {}"\
                               .format(dataset_name, viewing_area, dataset_level))
    return choropleth_map

def get_choropleth_map_by_id(choropleth_chart_id: int) -> ChoroplethMap:
    choropleth_map: ChoroplethMap = ChoroplethMap.query.filter_by(id = choropleth_chart_id).first()
    if not choropleth_map:
        raise ResourceNotFound("Could not find choropleth map with id = {}".format(choropleth_chart_id))
    return choropleth_map

def get_all_charts() -> list:
    charts = [ChartsResponse.from_chart(chart) for chart in Chart.query.all()]
    if not charts:
        raise ResourceNotFound("Could not find any charts")
    return charts

def get_chart_by_id(chart_id: int) -> Chart:
    chart: Chart = Chart.query.filter_by(id = chart_id).first()
    if not chart:
        raise ResourceNotFound("Could not find chart with id = {}".format(chart_id))
    return chart
