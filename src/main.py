"""NASA Space Apps 2022 Challenge
Team: Space Jam
Challenge: Take Flight: Making the Most of NASA’s Airborne Data
Authors Listed in Alphabetical Order
@Author: Akim Niyo <akimniyo27@gmail.com>, Fernando Rubio Garcia <fernando.rubiogarcia96@gmail.com>,
@Author: Grant Johnson <grantjohnson654@gmail.com>, Greg Heiman <gregheiman02@gmail.com>, 
@Author: Murphy Ownbey <wmownbey4@gmail.com>
@Date: 2022-10-01
"""
from datetime import datetime
from enum import Enum
from pathlib import Path

from flask import Flask, abort, jsonify

from src.google_cloud import generate_signed_url, upload_blob

app = Flask(__name__)

BUCKET_NAME = "nasa-space-apps-2022-graphs"
GC_AUTH_FILE = "space-app-364302-3ce902359f75.json"

class Datasets(Enum):
    """Enum for valid datasets that clients can query."""
    SEVERE_WEATHER=1
    AVG_SALARY=2

    @classmethod
    def value_of(cls, value):
        """Compare the value of a string to enum values."""
        # The class of enum to compare the string to.
        # cls = "your-enum-name"
        # The string value to compare.
        # value = "your-string=value"
        for k, v in cls.__members__.items():
            if k == value:
                return v
        else:
            raise ValueError(f"'{cls.__name__}' enum not found for '{value}'")

class GraphResponse:
    """Class representation of responses to graph requests."""
    dataset: str
    year: int
    filename: str
    callbackUrl: str

    def __init__(self, dataset: str, year: int, filename: str, callbackUrl: str):
        self.dataset = dataset
        self.year = year
        self.filename = filename
        self.callbackUrl = callbackUrl

    def to_dict(self):
        """Convert GraphResponse to a dictionary."""
        return {
            "dataset": graph_dataset,
            "year": year,
            "filename": dest_graph_filename,
            "callbackUrl": signed_url,
        }

def upload_and_gen_signed_url_for_graph(created_graph_filename: str):
        """Upload created graph to Google Cloud bucket and retrieve a signed URL for it."""
        # The local filename to upload to Google Cloud.
        # created_graph_filename = "your-created-graph-filename"
        # File name format: dataset-year-current_time.png
        dest_graph_filename = "{}-{}-{}.png".format(graph_dataset, year, datetime.now().strftime("%Y%m%d%H%M%S"))
        upload_blob(BUCKET_NAME, created_graph, dest_graph_filename) # Upload the created graph to GC
        signed_url = generate_signed_url(GC_AUTH_FILE, BUCKET_NAME, dest_graph_filename) # Get the graph from google cloud
        return (dest_graph_filename, signed_url)

@app.route("/api/graph/dataset/<string:graph_dataset>/year/<int:year>")
def create_graph_from_dataset_and_year(graph_dataset: str, year: int):
        """Create a graph from the desired dataset and year and return a GraphResponse to the client."""
        # The desired dataset for the graph.
        # graph_dataset = "your-desired-graph-dataset"
        # The desired year for the dataset.
        # year = "2022"
        try:
            Datasets.value_of(graph_dataset)
        except ValueError as e:
            abort(400, description=str(e))

        # created_graph # TODO (Greg Heiman): Generate the graph
        dest_graph_filename, signed_url = upload_and_gen_signed_url_for_graph(created_graph)
        graph_response = GraphResponse(graph_dataset, year, dest_graph_filename, signed_url)
        return jsonify(graph_response.to_dict())

@app.route("/api/graph/correllation/x-dataset/<string:x_dataset>/y-dataset/<string:y_dataset>/year/<int:year>")
def create_correlation_graph_from_datasets(x_dataset: str, y_dataset: str, year: int):
        """Create a correlation graph between two datasets."""
        # The dataset that you desire to be on the x-axis.
        # x_dataset = "your-desired-graph-dataset"
        # The dataset that you desire to be on the y-axis.
        # y_dataset = "your-desired-graph-dataset"
        # The year for both datasets.
        # year = "2022"
        try:
            Datasets.value_of(x_dataset)
            Datasets.value_of(y_dataset)
        except ValueError as e:
            abort(400, description=str(e))

        # created_graph # TODO (Greg Heiman): Generate correlation graph from both datasets
        graph_dataset = "{}/{} Correllation".format(x_dataset, y_dataset)
        dest_graph_filename, signed_url = upload_and_gen_signed_url_for_graph(created_graph)
        graph_response = GraphResponse(graph_dataset, year, dest_graph_filename, signed_url)
        return jsonify(graph_response.to_dict())

@app.route("/api/google-cloud/filename/<string:filename>")
def get_google_cloud_signed_url(filename: str):
        """Create a signed URL for a Google Cloud Bucket entity."""
        # The name of the file on Google Cloud
        # filename = "your-filename"
        signed_url = generate_signed_url(GC_AUTH_FILE, BUCKET_NAME, filename)

        if signed_url is None:
            abort(404, description="Could not generate signed URL for filename: {}".format(filename))

        return jsonify({
            "filename": filename,
            "callbackUrl": signed_url,
        })

@app.errorhandler(400)
def bad_request_parameters(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(401)
def invalid_credentials(e):
    return jsonify(error=str(e)), 401

@app.errorhandler(403)
def forbidden(e):
    return jsonify(error=str(e)), 403

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500

def main():
    # Setup web server. Runs on port 5000
    app.run()

if __name__ == "__main__":
    main()
