from src.models.choropleth_map import ChoroplethMap
from src.models.chart import Chart
from src.utils.google_cloud import generate_signed_url
from src.utils.constants import GC_AUTH_FILE, GC_BUCKET_NAME

class ChartsResponse:
    id: int
    type: str
    title: str
    subtitle: str
    url: str

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

def map_from_chart_to_charts_response(chart: Chart) -> ChartsResponse:
    chart_response = ChartsResponse
    chart_response.id = chart.id
    chart_response.type = chart.type
    chart_response.title = chart.title
    chart_response.subtitle = chart.subtitle
    chart_response.url = chart.chart_url()

    return chart_response

def _fix_choropleth_uri(chart: ChoroplethMap) -> ChoroplethMap:
    # If the URIs don't contain http:// or https:// then assume they are files in GC
    if "http://" not in chart.geo_data_uri or "https://" not in chart.geo_data_uri:
        chart.geo_data_uri = generate_signed_url(GC_AUTH_FILE, GC_BUCKET_NAME, chart.geo_data_uri)
    if "http://" not in chart.z_data_uri or "https://" not in chart.z_data_uri:
        chart.z_data_uri = generate_signed_url(GC_AUTH_FILE, GC_BUCKET_NAME, chart.z_data_uri)

    return chart

def get_choropleth_map(dataset_name: str, viewing_area: str, dataset_level: str) -> ChoroplethMap:
    choropleth_map: ChoroplethMap = ChoroplethMap.query.filter_by(dataset_name = dataset_name)\
    .filter_by(viewing_area_name = viewing_area)\
    .filter_by(dataset_level = dataset_level).first()

    choropleth_map = _fix_choropleth_uri(choropleth_map);
    return choropleth_map

def get_all_charts() -> list[ChartsResponse]:
    charts = Chart.query.all()

    chart_responses = []
    for chart in charts:
        chart_response = map_from_chart_to_charts_response(chart)
        chart_responses.append(chart_response)
    return chart_responses
