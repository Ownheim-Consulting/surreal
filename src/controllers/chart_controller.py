from flask import jsonify, Blueprint

from src.exceptions.http_error_response import ResourceNotFound, BadRequestParameters
from src.models.datasets import WeatherDatasets, EconomicDatasets, ViewingAreas, DatasetLevels
from src.services.chart_service import get_choropleth_map

chart_controller_blueprint = Blueprint('charts', __name__)

@chart_controller_blueprint.get("/api/chart/choropleth-map/dataset/<string:dataset_name>/viewing-area/<string:viewing_area>/level/<string:dataset_level>")
def get_choropleth_map_for_dataset(dataset_name: (WeatherDatasets or EconomicDatasets), viewing_area: ViewingAreas, dataset_level: DatasetLevels):
    if dataset_name not in WeatherDatasets and dataset_name not in EconomicDatasets:
        raise BadRequestParameters("Dataset name: {} is not a valid dataset name.".format(dataset_name))
    if viewing_area not in ViewingAreas:
        raise BadRequestParameters("Viewing area not a valid viewing area: {}".format(viewing_area))
    if dataset_level not in DatasetLevels:
        raise BadRequestParameters("Dataset level not a valid dataset level: {}".format(dataset_level))

    choropleth_map = get_choropleth_map(dataset_name, viewing_area, dataset_level)

    if choropleth_map is None:
        raise ResourceNotFound("Could not find choropleth map for dataset: {}".format(dataset_name))

    response = jsonify(choropleth_map.to_dict())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
