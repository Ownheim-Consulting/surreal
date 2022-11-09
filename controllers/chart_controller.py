from flask import Blueprint, jsonify, Response

from exceptions.http_error_response import ResourceNotFound, BadRequestParameters
from models.datasets import WeatherDatasets, EconomicDatasets, ViewingAreas, DatasetLevels
from models.choropleth_map import ChoroplethMap
import services.chart_service as chart_service

chart_controller_blueprint = Blueprint('charts', __name__)

@chart_controller_blueprint.get("/api/chart/choropleth-map/dataset/<string:dataset_name>/viewing-area/<string:viewing_area>/level/<string:dataset_level>")
def get_choropleth_map_for_dataset(dataset_name: (WeatherDatasets or EconomicDatasets),
                                   viewing_area: ViewingAreas,
                                   dataset_level: DatasetLevels) -> Response:
    if dataset_name not in WeatherDatasets and dataset_name not in EconomicDatasets:
        raise BadRequestParameters("Dataset name: {} is not a valid dataset name.".format(dataset_name))
    if viewing_area not in ViewingAreas:
        raise BadRequestParameters("Viewing area not a valid viewing area: {}".format(viewing_area))
    if dataset_level not in DatasetLevels:
        raise BadRequestParameters("Dataset level not a valid dataset level: {}".format(dataset_level))

    choropleth_map: ChoroplethMap = chart_service.get_choropleth_map(dataset_name, viewing_area, dataset_level)
    return jsonify(choropleth_map.to_dict())

@chart_controller_blueprint.get("/api/charts")
def charts() -> Response:
    charts: list = chart_service.get_all_charts()
    return jsonify([chart.to_dict() for chart in charts])
