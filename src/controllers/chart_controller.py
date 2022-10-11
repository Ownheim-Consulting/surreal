from flask import jsonify, Blueprint

from src.exceptions.http_error_response import ResourceNotFound, BadRequestParameters
from src.models.heat_map import HeatMap
from src.models.datasets import WeatherDatasets, EconomicDatasets

chart_controller_blueprint = Blueprint('charts', __name__)

@chart_controller_blueprint.get("/api/chart/heat-map/dataset/<string:dataset_name>")
def get_heatmap_for_dataset(dataset_name: str):
    if dataset_name not in WeatherDatasets or dataset_name not in EconomicDatasets:
        raise BadRequestParameters("Dataset name: {} is not a valid dataset name.".format(dataset_name))

    # Get the heat map from the database or generate it
    heat_map = HeatMap.query.filter_by(title = dataset_name).first()

    if heat_map is None:
        raise ResourceNotFound("Could not find heatmap for dataset: {}".format(dataset_name))

    return jsonify(heat_map.to_dict())
