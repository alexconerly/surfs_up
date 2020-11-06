import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Use create_engine which allows us to access the SQLite database:
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

#Use .pepare() to reflect our database:
Base.prepare(engine, reflect=True)

#Create a variable for each of the classes so that we can reference them later:
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create a session link from Python to our database:
session = Session(engine)

#To define our Flask app, create a Flask application called "app."
app = Flask(__name__)

#Define the welcome route:
@app.route("/")

#Add the routing information for each of the other routes
def welcome():
    return(
    f"Welcome to the Climate Analysis API!<br/>"
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/temp/start/end<br/>")

#Create Precipitation Route:
@app.route("/api/v1.0/precipitation")
#Create the Precipitation function
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#Create Stations Route:
@app.route("/api/v1.0/stations")
#Create the Precipitation function:
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#Create Temperature Route:
@app.route("/api/v1.0/tobs")
#Create the monthly Temperature Function:
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


#Create routes for starting and ending date:
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
#Create stats function:
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

    if not end: 
        results = session.query(*sel).\
        filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
