from flask import Flask, render_template, jsonify
from src.sensors import get_real_sensor_data

app = Flask(__name__)

@app.route('/')
def dashboard():
    """ Renders the HVAC monitoring dashboard """
    return render_template('dashboard.html')

@app.route('/sensor_data')
def sensor_data():
    """ Returns real-time sensor data as JSON """
    data = get_real_sensor_data()
    return jsonify(data)

def start_web_app():
    """ Runs the Flask web app on port 5000 """
    app.run(host='0.0.0.0', port=5000, debug=True)
