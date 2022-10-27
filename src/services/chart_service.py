from src.models.choropleth_map import ChoroplethMap
from src.google_cloud import generate_signed_url
from src.constants import GC_AUTH_FILE, GC_BUCKET_NAME
from src.models.datasets import EconomicDatasets, WeatherDatasets, ViewingAreas, DatasetLevels

def get_choropleth_map(dataset_name: str, viewing_area: str, dataset_level: str) -> ChoroplethMap:
    choropleth_map: ChoroplethMap = ChoroplethMap.query.filter_by(dataset_name = dataset_name)\
    .filter_by(viewing_area_name = viewing_area)\
    .filter_by(dataset_level = dataset_level).first()

    # If the URIs don't contain http:// or https:// then assume they are files in GC
    if "http://" not in choropleth_map.geo_data_uri or "https://" not in choropleth_map.geo_data_uri:
        choropleth_map.geo_data_uri = generate_signed_url(GC_AUTH_FILE, GC_BUCKET_NAME, choropleth_map.geo_data_uri)
    if "http://" not in choropleth_map.z_data_uri or "https://" not in choropleth_map.z_data_uri:
        choropleth_map.z_data_uri = generate_signed_url(GC_AUTH_FILE, GC_BUCKET_NAME, choropleth_map.z_data_uri)

    return choropleth_map
