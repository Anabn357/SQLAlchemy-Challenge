#################################################
# Dependencies
#################################################

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    """Return a list of rain fall for prior year"""

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    rain = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > last_year).\
        order_by(Measurement.date).all()

    
    rain_totals = []
    for result in rain:
        row = {}
        row["date"] = rain[0]
        row["prcp"] = rain[1]
        rain_totals.append(row)
     
    session.close()

    return jsonify(rain_totals)
#################################################                             
                             
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    """Return a list of all station names"""
    
    results = session.query(Station.name).all()

    station_names = list(np.ravel(results))
    
    session.close()

    return jsonify(station_names)

#################################################                             
                             
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    """Return a list of temperatures for prior year"""

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > last_year).\
        order_by(Measurement.date).all()

    temperature_totals = []
    for result in temperature:
        row = {}
        row["date"] = temperature[0]
        row["tobs"] = temperature[1]
        temperature_totals.append(row)
    
    session.close()

    return jsonify(temperature_totals)

#################################################                             

@app.route("/api/v1.0/<start>")
def temperatures_start(start):
    session = Session(engine)
                             
    """ Given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than 
        and equal to the start date. 
    """
    
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    
    session.close()

   
    temperatures_start = list(np.ravel(results))

    return jsonify(temperatures_start)

#################################################                             

@app.route("/api/v1.0/<start>/<end>")                            
def temperatures_start_end(start, end):
    
    session = Session(engine)
    
    """ When given the start and the end date, calculate the TMIN, TAVG, 
        and TMAX for dates between the start and end date inclusive.
    """

    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    temperatures_start_end = list(np.ravel(results))

    return jsonify(temperatures_start_end)

#################################################  

                           

if __name__ == "__main__":
    app.run(debug=True)