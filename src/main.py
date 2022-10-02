from flask import Flask, abort, jsonify, Response

from domain.db import engine, Base, Session
from domain.CountyAvgSal import getCountyAvgSalByLatLng, getCountyAvgSalByName
from generate_signed_urls import generate_signed_url

app = Flask(__name__)
session = Session()

BUCKET_NAME = "nasa-space-apps-2022-graphs"
GC_AUTH_FILE = "./src/space-app-364302-3ce902359f75.json"

@app.route("/api/avgsal/lat/<float:lat>/lng/<float:lng>")
def getCountyAvgSal(lat: float, lng: float):
    countyAvgSal = getCountyAvgSalByLatLng(session, lat, lng)
    if countyAvgSal is None:
        abort(404, description="Could not retrieve CountyAvgSal with lat: {} and lng: {}".format(lat, lng))

    return jsonify(countyAvgSal.toDict())

@app.route("/api/avgsal/name/<string:name>")
def getCountyAvgSalUsingName(name: str):
    countyAvgSal = getCountyAvgSalByName(session, name)
    if countyAvgSal is None:
        abort(404, description="Could not retrieve CountyAvgSal with name: {}".format(name))

    return jsonify(countyAvgSal.toDict())

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
    # Create all of the DB tables if they don't exist
    Base.metadata.create_all(engine)

    # Setup web server. Runs on port 5000
    app.run()

if __name__ == "__main__":
    main()
