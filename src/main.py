"""NASA Space Apps 2022 Challenge
Team: Space Jam
Challenge: Take Flight: Making the Most of NASA’s Airborne Data
Authors Listed in Alphabetical Order
@Author: Akim Niyo <akimniyo27@gmail.com>, Dimitri Senevitratne <senevids@gmail.com>
@Author: Fernando Rubio Garcia <fernando.rubiogarcia96@gmail.com>, Grant Johnson <grantjohnson654@gmail.com>,
@Author: Greg Heiman <gregheiman02@gmail.com>, Murphy Ownbey <wmownbey4@gmail.com>
@Date: 2022-10-01
"""
from datetime import datetime
from enum import Enum
from pathlib import Path

from flask import Flask, abort, jsonify, render_template

from src.google_cloud import generate_signed_url, upload_blob
from src.exceptions.http_error_response import HttpErrorResponse, ResourceNotFound, InternalServerError

app = Flask(__name__)

BUCKET_NAME = "nasa-space-apps-2022-graphs"
GC_AUTH_FILE = "space-app-364302-3ce902359f75.json"

class ChartResponse:
    """Class representation of responses to graph requests."""
    chart_tite: str
    chart_data: str

    def __init__(self, chart_title: str, chart_data: str):
        self.chart_tite = chart_title
        self.chart_data = chart_data

    def to_dict(self):
        """Convert GraphResponse to a dictionary."""
        return {
            "chart_title": chart_title,
            "chart_data": chart_data,
        }

@app.errorhandler(HttpErrorResponse)
def handle_http_error_response(e):
    """Return JSON instead of HTML for HTTP errors."""
    return jsonify(e.to_dict())

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(ResourceNotFound("Could not find desired resource. Ensure URL is correct.").to_dict())

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle non-HTTP exceptions."""
    # pass through HTTP errors
    if isinstance(e, HttpErrorResponse):
        return e
    # now you're handling non-HTTP exceptions only
    return jsonify(InternalServerError("Undefined Internal Server Error").to_dict())

@app.route("/api/google-cloud/filename/<string:filename>")
def get_google_cloud_signed_url(filename: str):
        """Create a signed URL for a Google Cloud Bucket entity."""
        # The name of the file on Google Cloud
        # filename = "your-filename"
        signed_url = generate_signed_url(GC_AUTH_FILE, BUCKET_NAME, filename)

        if signed_url is None:
            raise ResourceNotFound("Could not generate signed URL for filename: {}".format(filename))

        return jsonify({
            "filename": filename,
            "callbackUrl": signed_url,
        })

def main():
    # Setup web server. Runs on port 5000
    app.run()

if __name__ == "__main__":
    main()
