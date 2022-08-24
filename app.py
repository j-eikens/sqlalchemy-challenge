import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

##Database setup
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect tables
Base = automap_base()
Base.prepare(engine, reflect=True)

#create classes
Measurement = Base.classes.measurement
Station = Base.classes.station


##Flask Setup
app = Flask(__name__)

@app.route("/")
def home():
    """List all available api routes."""
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)

    #query for precipation in last 12 months of data
    past_year = session.query(Measurement.date, Measurement.prcp).where(Measurement.date >= '2016-08-23')

    session.close()

    #create lists of dates and precipitation
    prcp_date = []
    
    for date, prcp in past_year:
        
        prcp_date_dict = {}
        
        prcp_date_dict['date'] = date
        prcp_date_dict['prcp'] = prcp

        prcp_date.append(prcp_date_dict)

    return jsonify(prcp_date)    

    
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    station_query = session.query(Station.name).all()

    session.close()

    station_list = list(np.ravel(station_query))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    US00519281_12mo = session.query(Measurement.date, Measurement.tobs).where(Measurement.date >= '2016-08-18')

    session.close()

    temp_list = []

    for i in US00519281_12mo:   

        temp = i[1]    
        temp_list.append(temp)

    return jsonify(temp_list)

# @app.route("/api/v1.0/<start>")
# def start(start):
#     session = Session(engine)

#     query = session.query(Measurement.station, Measurement.date,\
#                                 func.max(Measurement.tobs),\
#                                 func.min(Measurement.tobs),\
#                                 func.avg(Measurement.tobs)).\
#                                 where(Measurement.date >= start).all()

#     session.close()

#     temp_list = []

#     for i in query:
#         temp = i[1] 
#         temp_list.append(temp)
    

#     return jsonify(temp_list)

if __name__ == "__main__":
    app.run(debug=True)