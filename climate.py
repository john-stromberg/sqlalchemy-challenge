# import dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#database connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)
@app.route("/")
def home():
    return(
        f"Welcome to climate api<br/>"
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    prcp_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > one_year).order_by(Measurement.date).all()
    return jsonify(prcp_scores)

@app.route("/api/v1.0/stations")
def stations():
    all_stations = session.query(Station.station, Station.name).all()
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_year = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= one_year).all()
    return jsonify(tobs_year)

@app.route("/api/v1.0/<start>")
def start_date_only(date):
    temp_results =  session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= date).all()
    return jsonify(temp_results)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    temp_results_range = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(temp_results_range)

if __name__ == "__main__":
    app.run(debug=True)






