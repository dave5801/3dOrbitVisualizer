from flask import Flask, jsonify, render_template
import numpy as np

app = Flask(__name__)

# Function to generate orbital points
def generate_orbit(a, e, num_points=500):
    theta = np.linspace(0, 2 * np.pi, num_points)
    r = a * (1 - e**2) / (1 + e * np.cos(theta))
    
    x = list(r * np.cos(theta))
    y = list(r * np.sin(theta))
    z = [0] * len(x)  # Keep Z as 0 for simplicity

    return {"x": x, "y": y, "z": z}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/orbit-data")
def orbit_data():
    orbit = generate_orbit(10, 0.3)  # Semi-major axis = 10, Eccentricity = 0.3
    return jsonify(orbit)

if __name__ == "__main__":
    app.run(debug=True)
