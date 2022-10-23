from src.models.geo_heat_map import GeoHeatMap
from src.google_cloud import generate_signed_url
from src.constants import GC_AUTH_FILE, GC_BUCKET_NAME

def get_choropleth_map(dataset_name: str, viewing_area:str, dataset_level: str):
    choropleth_map: GeoHeatMap = GeoHeatMap.query.filter_by(dataset_name = dataset_name).filter_by(viewing_area_name = viewing_area).filter_by(dataset_level = dataset_level).first()

    # If the URIs don't contain http:// or https:// then assume they are files in GC
    if "http://" not in choropleth_map.geojson_uri or "https://" not in choropleth_map.geojson_uri:
        choropleth_map.geojson_uri = generate_signed_url(GC_AUTH_FILE, GC_BUCKET_NAME, choropleth_map.geojson_uri)
    if "http://" not in choropleth_map.zjson_uri or "https://" not in choropleth_map.zjson_uri:
        choropleth_map.zjson_uri = generate_signed_url(GC_AUTH_FILE, GC_BUCKET_NAME, choropleth_map.zjson_uri)

    return choropleth_map
