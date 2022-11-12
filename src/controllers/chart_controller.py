from flask import jsonify, Blueprint

from src.exceptions.http_error_response import ResourceNotFound, BadRequestParameters
from src.models.datasets import WeatherDatasets, EconomicDatasets, ViewingAreas, DatasetLevels
import src.services.chart_service as chart_service

chart_controller_blueprint = Blueprint('charts', __name__)

@chart_controller_blueprint.get("/api/chart/choropleth-map/dataset/<string:dataset_name>/viewing-area/<string:viewing_area>/level/<string:dataset_level>")
def get_choropleth_map_for_dataset(dataset_name: (WeatherDatasets or EconomicDatasets), viewing_area: ViewingAreas, dataset_level: DatasetLevels):
    if dataset_name not in WeatherDatasets and dataset_name not in EconomicDatasets:
        raise BadRequestParameters("Dataset name: {} is not a valid dataset name.".format(dataset_name))
    if viewing_area not in ViewingAreas:
        raise BadRequestParameters("Viewing area not a valid viewing area: {}".format(viewing_area))
    if dataset_level not in DatasetLevels:
        raise BadRequestParameters("Dataset level not a valid dataset level: {}".format(dataset_level))

    choropleth_map = chart_service.get_choropleth_map(dataset_name, viewing_area, dataset_level)

    if not choropleth_map:
        raise ResourceNotFound("Could not find choropleth map for dataset: {}, viewing-area: {}, and dataset-level: {}"\
                               .format(dataset_name, viewing_area, dataset_level))
    return jsonify(choropleth_map.to_dict())

@chart_controller_blueprint.get("/api/chart/choropleth-map/<int:choropleth_chart_id>")
def get_choropleth_map(choropleth_chart_id: int) -> Response:
    choropleth_map: ChoroplethMap = chart_service.get_choropleth_map_by_id(choropleth_chart_id)
    return choropleth_map

@chart_controller_blueprint.get("/api/chart/<int:chart_id>")
def get_chart(chart_id: int) -> Response:
    chart: Chart = chart_service.get_chart_by_id(chart_id)
    return jsonify(chart.to_dict())

@chart_controller_blueprint.get("/api/charts")
def charts():
    charts = chart_service.get_all_charts()

    if not charts:
        raise ResourceNotFound("Could not find any charts")
    return jsonify([chart.to_dict() for chart in charts])
