from flask import jsonify, Blueprint

from src.exceptions.http_error_response import ResourceNotFound, BadRequestParameters
from src.models.geo_heat_map import GeoHeatMap
from src.models.datasets import WeatherDatasets, EconomicDatasets, ViewingAreas, DatasetLevels

chart_controller_blueprint = Blueprint('charts', __name__)

@chart_controller_blueprint.get("/api/chart/geo-heat-map/dataset/<string:dataset_name>/viewing-area/<string:viewing_area>/level/<string:dataset_level>")
def get_heatmap_for_dataset(dataset_name: str, viewing_area: str, dataset_level: str):
    if dataset_name not in WeatherDatasets and dataset_name not in EconomicDatasets:
        raise BadRequestParameters("Dataset name: {} is not a valid dataset name.".format(dataset_name))
    if viewing_area not in ViewingAreas:
        raise BadRequestParameters("Viewing area not a valid viewing area: {}".format(viewing_area))
    if dataset_level not in DatasetLevels:
        raise BadRequestParameters("Dataset level not a valid dataset level: {}".format(dataset_level))

    # Get the heat map from the database or generate it
    heat_map = GeoHeatMap.query.filter_by(dataset_name = dataset_name).filter_by(viewing_area_name = viewing_area).filter_by(dataset_level = dataset_level).first()

    if heat_map is None:
        raise ResourceNotFound("Could not find heatmap for dataset: {}".format(dataset_name))

    return jsonify(heat_map.to_dict())
