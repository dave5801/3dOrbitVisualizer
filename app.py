from flask import Flask, render_template, jsonify
from skyfield.api import load, EarthSatellite
import numpy as np
import requests

app = Flask(__name__)

# Load satellite data (Sample ISS TLE)
'''
TLE_LINE1 = "1 25544U 98067A   24036.54270833  .00016717  00000+0  30447-3 0  9991"
TLE_LINE2 = "2 25544  51.6438  66.4836 0004175  45.6977  64.2249 15.50359495441068"

ts = load.timescale()
satellite = EarthSatellite(TLE_LINE1, TLE_LINE2, "ISS", ts)
'''

def get_satellite_position(tle_lines):
    ts = load.timescale()
    satellite = EarthSatellite(tle_lines[0], tle_lines[1], "Satellite", ts)
    t = ts.now()
    geocentric = satellite.at(t)
    subpoint = geocentric.subpoint()
    return {
        "latitude": subpoint.latitude.degrees,
        "longitude": subpoint.longitude.degrees,
        "altitude": subpoint.elevation.km
    }

'''
def compute_orbit():
    # Load the timescale object
    ts = load.timescale()
    times = ts.utc(2024, 2, np.linspace(0, 24, 100))  # Compute over 24 hours
    geocentric_positions = satellite.at(times).position.km  # Get (x, y, z) in km
    return geocentric_positions.tolist()'''

def get_tle(satellite_id):
    url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={satellite_id}&FORMAT=tle"
    response = requests.get(url)
    return response.text.split("\n")[:2]  # Return first two lines of TLE

@app.route('/')
def index():
    return render_template('index.html')
'''
@app.route('/orbit_data')
def orbit_data():
    return jsonify(compute_orbit())
    '''

@app.route('/satellite_position')
def satellite_position():
    satellite_tle = get_tle(25544) # Example for ISS
    sat_position = get_satellite_position(satellite_tle)
    return jsonify(sat_position)

if __name__ == '__main__':
    app.run(debug=True)
