from src.models.choropleth_map import ChoroplethMap
from src.models.chart import Chart
from src.utils.google_cloud import generate_signed_url
from src.utils.constants import GC_AUTH_FILE, GC_BUCKET_NAME

class ChartsResponse:
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

def _fix_uri_with_signed_url(*uris):
    # Add signed uri for file if it is missing http:// or https://
    # If the URIs don't contain http:// or https:// then assume they are files in GC
    uris = [generate_signed_url(GC_AUTH_FILE, GC_BUCKET_NAME, uri) if ('http://' not in uri or 'https://' not in uri) else uri for uri in uris]
    return uris

def get_choropleth_map(dataset_name: str, viewing_area: str, dataset_level: str) -> ChoroplethMap:
    choropleth_map: ChoroplethMap = ChoroplethMap.query.filter_by(dataset_name = dataset_name)\
    .filter_by(viewing_area_name = viewing_area)\
    .filter_by(dataset_level = dataset_level).first()

    (choropleth_map.geo_data_uri, choropleth_map.z_data_uri) = _fix_uri_with_signed_url(choropleth_map.geo_data_uri, choropleth_map.z_data_uri)
    return choropleth_map

def get_all_charts() -> list:
    charts = Chart.query.all()

    chart_responses = []
    for chart in charts:
        chart_response = ChartsResponse.from_chart(chart)
        chart_responses.append(chart_response)
    return chart_responses
