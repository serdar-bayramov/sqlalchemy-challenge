import numpy as np
import os
import datetime as dt
from datetime import datetime

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

# create route to return station names
@app.route("/api/v1.0/stations")
def station():
    session=Session(engine)
    station_names = session.query(Station.name).all()
    session.close()

    station_list = []
    for names in station_names:
        station_list.append([name for name in names])
    return jsonify(station_list)

# create route to return temp observations
@app.route("/api/v1.0/tobs")
def temperature():
    session=Session(engine)

    last_date=session.query(Measurement.date).group_by(Measurement.date).order_by((Measurement.date).desc()).first()
    last_date=last_date.date
    last_year = datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
    temp_observation = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>last_year).filter(Measurement.station=='USC00519281').all()
    session.close()

    temp_list = []
    for date, temp in temp_observation:
        temp_dict={}
        temp_dict['date']=date
        temp_dict['temp']=temp
        temp_list.append(temp_dict)
    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)









