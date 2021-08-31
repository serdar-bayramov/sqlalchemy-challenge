import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from sqlalchemy.sql.roles import StatementOptionRole

# Database Setup

file_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
db_path = f"sqlite:///{file_dir}/hawaii.sqlite"
engine = create_engine(db_path)

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect=True)
print(Base.classes.keys())

# save reference to the table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask set up

app = Flask(__name__)

@app.route("/")
def home():
    return(
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start><br/>"
    f"/api/v1.0/<start>/<end>")

#create route to return dictionary in json format with date and precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)
    prcp_result = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    prcp_list = []
    for date, prcp in prcp_result:
        prcp_dict={}
        prcp_dict['date']=date
        prcp_dict['prcp']=prcp
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)

# create route to retun station names
@app.route("/api/v1.0/stations")
def station():
    session=Session(engine)
    station_names = session.query(Station.name).all()
    session.close()

    station_list = []
    for names in station_names:
        station_list.append([name for name in names])
    return jsonify(station_list)


if __name__ == '__main__':
    app.run(debug=True)









