from flask import Flask, abort, jsonify, Response

from domain.db import engine, Base, Session
from domain.CountyAvgSal import getCountyAvgSalByLatLng, getCountyAvgSalByName

app = Flask(__name__)
session = Session()

class ErrorResponse:
    code: int
    error: str
    message: str

    def __init__(self, code: int, error: str, message: str):
        self.code = code
        self.error = error
        self.message = message

    def toJson(self):
        return {
            "code": self.code,
            "error": self.error,
            "message": self.message
        }

@app.route("/api/avgsal/lat/<float:lat>/lng/<float:lng>")
def getCountyAvgSalByLatLng(lat: float, lng: float):
    countyAvgSal = getCountyAvgSalByLatLng(session, lat, lng)
    if countyAvgSal is None:
        e = ErrorResponse(404, "RESOURCE_NOT_FOUND", "Could not retrieve CountyAvgSal with lat: {} and lng: {}".format(lat, lng))
        return jsonify(e.toJson()), e.code

    return jsonify(countyAvgSal.toJson())

@app.route("/api/avgsal/name/<string:name>")
def getCountyAvgSalByName(name):
    countyAvgSal = getCountyAvgSalByName(session, name)
    if countyAvgSal is None:
        e = ErrorResponse(404, "RESOURCE_NOT_FOUND", "Could not retrieve CountyAvgSal with name: {}".format(name))
        return jsonify(e.toJson()), e.code

    return jsonify(countyAvgSal.toJson())

def getCountyAvgSal(lat, lng):
    countyAvgSal = getCountyAvgSalByLatLng(session, lat, lng)
    if countyAvgSal is None:
        e = ErrorResponse(404, "RESOURCE_NOT_FOUND", "Could not retrieve CountyAvgSal with lat: {} and lng: {}".format(lat, lng))
        return jsonify(e.toJson()), e.code

    return jsonify(countyAvgSal.toJson())
def main():
    # Create all of the DB tables if they don't exist
    Base.metadata.create_all(engine)

    # Setup web server. Runs on port 5000
    app.run()

if __name__ == "__main__":
    main()
