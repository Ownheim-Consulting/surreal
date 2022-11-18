from database import db_session as session
from exceptions.http_error_response import BadRequestParameters
from models.datasets import WeatherDatasets, EconomicDatasets, ViewingAreas, DatasetLevels
from models.choropleth_map import ChoroplethMap
from models.chart import Chart
from repos.sqlalchemy_repo import SqlAlchemyRepo
import services.chart_service as chart_service

from flask import Blueprint, jsonify, Response

chart_controller_blueprint = Blueprint('charts', __name__)

@chart_controller_blueprint.get('/chart/choropleth-map/dataset/<string:dataset_name>/viewing-area/<string:viewing_area>/level/<string:dataset_level>')
def get_choropleth_map_for_dataset(dataset_name: (WeatherDatasets or EconomicDatasets),
                                   viewing_area: ViewingAreas,
                                   dataset_level: DatasetLevels) -> Response:
    if dataset_name not in WeatherDatasets and dataset_name not in EconomicDatasets:
        raise BadRequestParameters('Dataset name: {} is not a valid dataset name.'.format(dataset_name))
    if viewing_area not in ViewingAreas:
        raise BadRequestParameters('Viewing area not a valid viewing area: {}'.format(viewing_area))
    if dataset_level not in DatasetLevels:
        raise BadRequestParameters('Dataset level not a valid dataset level: {}'.format(dataset_level))

    repo: SqlAlchemyRepo = SqlAlchemyRepo[ChoroplethMap](session, ChoroplethMap)
    choropleth_map: ChoroplethMap = chart_service.get_choropleth_map(repo, dataset_name, viewing_area, dataset_level)
    return jsonify(choropleth_map.to_dict())

@chart_controller_blueprint.get('/chart/choropleth-map/<int:choropleth_chart_id>')
def get_choropleth_map(choropleth_chart_id: int) -> Response:
    repo: SqlAlchemyRepo = SqlAlchemyRepo(session, ChoroplethMap)
    choropleth_map: ChoroplethMap = chart_service.get_choropleth_map_by_id(repo, choropleth_chart_id)
    return jsonify(choropleth_map.to_dict())

@chart_controller_blueprint.get('/chart/<int:chart_id>')
def get_chart(chart_id: int) -> Response:
    repo: SqlAlchemyRepo = SqlAlchemyRepo(session, Chart)
    chart: Chart = chart_service.get_chart_by_id(repo, chart_id)
    return jsonify(chart.to_dict())

@chart_controller_blueprint.get('/charts')
def charts() -> Response:
    repo: SqlAlchemyRepo = SqlAlchemyRepo(session, Chart)
    charts: list = chart_service.get_all_charts(repo)
    return jsonify([chart.to_dict() for chart in charts])
