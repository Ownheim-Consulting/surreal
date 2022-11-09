"""NASA Space Apps 2022 Challenge
Team: Space Jam
Challenge: Take Flight: Making the Most of NASA’s Airborne Data
Authors Listed in Alphabetical Order
@Author: Akim Niyo <akimniyo27@gmail.com>, Dimitri Senevitratne <senevids@gmail.com>
@Author: Fernando Rubio Garcia <fernando.rubiogarcia96@gmail.com>, Grant Johnson <grantjohnson654@gmail.com>,
@Author: Greg Heiman <gregheiman02@gmail.com>, Murphy Ownbey <wmownbey4@gmail.com>
@Date: 2022-10-01
"""
from flask import abort, Flask, jsonify, Response

from controllers.chart_controller import chart_controller_blueprint
from controllers.google_cloud_controller import google_cloud_controller_blueprint 
from database import init_db, db_session
from exceptions.http_error_response import HttpErrorResponse, ResourceNotFound, InternalServerError
from utils.constants import GC_AUTH_FILE, GC_BUCKET_NAME

app = Flask(__name__)
app.register_blueprint(chart_controller_blueprint)
app.register_blueprint(google_cloud_controller_blueprint)

@app.teardown_appcontext
def shutdown_session(exception=None) -> None:
    db_session.remove()

@app.errorhandler(HttpErrorResponse)
def handle_http_error_response(e: HttpErrorResponse) -> Response:
    """Return JSON instead of HTML for HTTP errors."""
    return jsonify(e.to_dict())

@app.errorhandler(404)
def resource_not_found(e: Exception) -> Response:
    return jsonify(ResourceNotFound("Could not find desired resource. Ensure URL is correct.").to_dict())

@app.errorhandler(Exception)
def handle_exception(e: Exception) -> Response:
    """Handle non-HTTP exceptions."""
    # pass through HTTP errors
    if isinstance(e, HttpErrorResponse):
        return e
    # now you're handling non-HTTP exceptions only
    return jsonify(InternalServerError("Undefined Internal Server Error: {}".format(e)).to_dict())

@app.after_request
def after_request(response: Response) -> Response:
    """Perform logic on each response before sending it back to client."""
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def main() -> None:
    init_db()
    # Setup web server. Runs on port 5000
    app.run()

if __name__ == "__main__":
    main()
