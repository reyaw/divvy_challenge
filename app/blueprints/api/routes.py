from flask.globals import request
from .import bp as api
from .models import Divvy
from flask import render_template
from datetime import datetime
import statistics

@api.route('/')
def home():
   return render_template('index.html')

@api.route('/calculate')
def get_average_duration():
    # Start Date
    start = request.args.get('start')
    # End Date
    end = request.args.get('end')
    # From Station ID (returns None if left blank)
    from_station_id = request.args.get('from_station_id')

    #If a station id has been provided
    if from_station_id:
        # Query the database for the Station Name
        from_station_name = Divvy.query.filter(Divvy.from_station_id == from_station_id).first().from_station_name

        # Query the database for records that have a starttime between the start and end dates, as well as the correct station id
        data = Divvy.query.filter(Divvy.starttime >= datetime.strptime(start, '%Y-%m-%d'),
                                  Divvy.starttime <= datetime.strptime(end, '%Y-%m-%d'), Divvy.from_station_id == from_station_id).all()

    else:
        # Query the database for records that have a starttime between the start and end dates
        data = Divvy.query.filter(Divvy.starttime >= datetime.strptime(start, '%Y-%m-%d'),
                                  Divvy.stoptime <= datetime.strptime(end, '%Y-%m-%d')).all()

    # Get the mean of the trip_duration column from our previous query
    avg_duration = round(statistics.mean([record.trip_duration for record in data]), 3)
    
    # Return JSON object
    return {
        'avg_duration':avg_duration,
        'from_station_id':from_station_id,
        'from_station_name': from_station_name
    } if from_station_id else {
        'avg_duration': avg_duration,
    }

