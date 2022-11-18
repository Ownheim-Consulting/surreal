from dataclasses import dataclass

from exceptions.http_error_response import ResourceNotFound
from models.chart import Chart
from models.choropleth_map import ChoroplethMap
from models.response_model import ResponseModel
from repos.base_repo import BaseRepo
import utils.google_cloud as GC

@dataclass
class ChartsResponse(ResponseModel):
    id: int
    type: str
    title: str
    subtitle: str

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'type': self.type,
        }

    @classmethod
    def from_chart(cls, chart: Chart):
        return cls(chart.id, chart.type, chart.title, chart.subtitle)

def get_choropleth_map(repo: BaseRepo[ChoroplethMap], dataset_name: str, viewing_area: str, dataset_level: str) -> ChoroplethMap:
    choropleth_map: ChoroplethMap = repo.get_by_params(dataset_name=dataset_name,
                                                       viewing_area_name=viewing_area,
                                                       dataset_level=dataset_level)

    if not choropleth_map:
        raise ResourceNotFound('Could not find choropleth map for dataset: {}, viewing-area: {}, and dataset-level: {}'\
                               .format(dataset_name, viewing_area, dataset_level))
    return choropleth_map

def get_choropleth_map_by_id(repo: BaseRepo[ChoroplethMap], choropleth_chart_id: int) -> ChoroplethMap:
    choropleth_map: ChoroplethMap = repo.get(choropleth_chart_id)
    if not choropleth_map:
        raise ResourceNotFound('Could not find choropleth map with id = {}'.format(choropleth_chart_id))
    return choropleth_map

def get_all_charts(repo: BaseRepo[Chart]) -> list:
    charts: list = [ChartsResponse.from_chart(chart) for chart in repo.get_all()]
    if not charts:
        raise ResourceNotFound('Could not find any charts')
    return charts

def get_chart_by_id(repo: BaseRepo[Chart], chart_id: int) -> Chart:
    chart: Chart = repo.get(chart_id)
    if not chart:
        raise ResourceNotFound('Could not find chart with id = {}'.format(chart_id))
    return chart
