from datetime import datetime

from flask import Flask, abort, jsonify, Response

from google_cloud import generate_signed_url, upload_blob

app = Flask(__name__)

BUCKET_NAME = "nasa-space-apps-2022-graphs"
GC_AUTH_FILE = "space-app-364302-3ce902359f75.json"

class GraphResponse:
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
        return {
            "dataset": graph_dataset,
            "year": year,
            "filename": dest_graph_filename,
            "callbackUrl": signed_url,
        }

def upload_and_gen_signed_url_for_graph(created_graph_filename: str):
        # File name format: dataset-year-current_time.png
        dest_graph_filename = "{}-{}-{}.png".format(graph_dataset, year, datetime.now().strftime("%Y%m%d%H%M%S"))
        upload_blob(BUCKET_NAME, created_graph, dest_graph_filename) # Upload the created graph to GC
        signed_url = generate_signed_url(GC_AUTH_FILE, BUCKET_NAME, dest_graph_filename) # Get the graph from google cloud
        return (dest_graph_filename, signed_url)

@app.route("/api/graph/dataset/<string:graph_dataset>/year/<int:year>")
def create_graph_from_dataset_and_year(graph_dataset: str, year: int):
        # Retrieve graph
        # created_graph # TODO (Greg Heiman): Generate the graph
        dest_graph_filename, signed_url = upload_and_gen_signed_url_for_graph(created_graph)
        graph_response = GraphResponse(graph_dataset, year, dest_graph_filename, signed_url)
        return jsonify(graph_response.to_dict())

@app.route("/api/graph/corellation/x-dataset/<string:x_dataset>/y-dataset/<string:y_dataset>")
def create_correlation_graph_from_datasets(x_dataset: str, y_dataset: str):
        # created_graph # TODO (Greg Heiman): Generate correlation graph from both datasets
        graph_dataset = "{}/{} Corellation".format(x_dataset, y_dataset)
        dest_graph_filename, signed_url = upload_and_gen_signed_url_for_graph(created_graph)
        graph_response = GraphResponse(graph_dataset, year, dest_graph_filename, signed_url)
        return jsonify(graph_response.to_dict())

@app.route("/api/google-cloud/filename/<string:filename>")
def get_google_cloud_signed_url(filename: str):
    signed_url = generate_signed_url(GC_AUTH_FILE, BUCKET_NAME, filename)

    if signed_url is None:
        abort(404, description="Could not generate signed URL for filename: {}".format(filename))

    return jsonify({
        "filename": filename,
        "callbackUrl": signed_url,
    })

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500

@app.errorhandler(403)
def forbidden(e):
    return jsonify(error=str(e)), 403

@app.errorhandler(401)
def invalid_credentials(e):
    return jsonify(error=str(e)), 401

def main():
    # Setup web server. Runs on port 5000
    app.run()

if __name__ == "__main__":
    main()
