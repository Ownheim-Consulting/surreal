from datetime import datetime

from flask import Flask, abort, jsonify, Response

from google_cloud import generate_signed_url, upload_blob

app = Flask(__name__)
session = Session()

BUCKET_NAME = "nasa-space-apps-2022-graphs"
GC_AUTH_FILE = "space-app-364302-3ce902359f75.json"

@app.route("/api/graph/dataset/<string:graph_dataset>/year/<int:year>")
def getGraphDatasetForYear(graph_dataset: str, year: int):
        # Retrieve graph
        # created_graph # TODO (Greg Heiman): Generate the graph
        # File name format: dataset-year-current_time.png
        dest_graph_filename = "{}-{}-{}.png".format(graph_dataset, year, datetime.now().strftime("%Y%m%d%H%M%S"))
        upload_blob(BUCKET_NAME, created_graph, dest_graph_filename)
        signed_url = generate_signed_url(GC_AUTH_FILE, BUCKET_NAME, dest_graph_filename) # Get the graph from GC
        return jsonify({
            "dataset": graph_dataset,
            "year": year,
            "filename": dest_graph_filename,
            "callbackUrl": signed_url,
        })

@app.route("/api/gc/filename/<string:filename>")
def getGcSignedUrl(filename: str):
    signed_url = generate_signed_url(GC_AUTH_FILE, BUCKET_NAME, filename)

    if signed_url is None:
        abort(404, description="Could not generate signed URL for filename: {}".format(filename))

    return jsonify({
        "filename": filename,
        "callbackUrl": signed_url,
    })

@app.errorhandler(404)
def resourceNotFound(e):
    return jsonify(error=str(e)), 404

def main():
    # Setup web server. Runs on port 5000
    app.run()

if __name__ == "__main__":
    main()
