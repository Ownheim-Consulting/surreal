from flask import Flask

from domain.db import engine, Base, Session
from domain.CountyAvgSal import getCountyAvgSalByLatLng

app = Flask(__name__)
session = Session()

@app.route("/api/avgsal/lat/<float:lat>/lng/<float:lng>")
def getCountyAvgSal(lat, lng, year):
    countyAvgSal = getCountyAvgSalByLatLng(session, lat, lng)
    return countyAvgSal

def main():
    # Create all of the DB tables if they don't exist
    Base.metadata.create_all(engine)

    # Setup web server. Runs on port 5000
    app.run()

if __name__ == "__main__":
    main()
