import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite", connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    """List all available api routes."""
    return (
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start (enter start date in the format YYYY-MM-DD in place of _start_; date is included in query)<br/>"
        "/api/v1.0/start/end (enter start and end dates in the format YYYY-MM-DD in place of _start_ and _end_; dates are included in query)"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the last year of precipitation data"""
    # Query precipitation data
    prcp_data = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date > '2016-08-22')\
        .order_by(Measurement.date).all()
    
    return jsonify(dict(prcp_data))

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    stations = session.query(Station.station).all()
    
    return jsonify(list(np.ravel(stations)))

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the last year of tobs data"""
    tobs_data = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.date > '2016-08-22')\
    .order_by(Measurement.date).all()
    
    return jsonify(dict(tobs_data))

@app.route("/api/v1.0/<start>")
def start(start):
    temp_aggs = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))\
        .filter(Measurement.date >= f"'{start}'")\
        .first()
    aggs_dict = {}
    aggs_dict["tmin"] = temp_aggs[0]
    aggs_dict["tmax"] = temp_aggs[1]
    aggs_dict["tavg"] = temp_aggs[2]
        
    return jsonify(aggs_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    temp_aggs = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))\
        .filter(Measurement.date >= f"'{start}'")\
        .filter(Measurement.date <= f"'{end}'")\
        .first()
    aggs_dict = {}
    aggs_dict["tmin"] = temp_aggs[0]
    aggs_dict["tmax"] = temp_aggs[1]
    aggs_dict["tavg"] = temp_aggs[2]
        
    return jsonify(aggs_dict)

if __name__ == '__main__':
    app.run(debug=True)
