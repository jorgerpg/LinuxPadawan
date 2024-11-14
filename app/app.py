import os
from flask import Flask, render_template, request
from sqlite import Database
from mqtt_client import MQTTClient
import logging

# Basic logging configuration to send everything to stdout
logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(levelname)s - %(message)s'
)
handler = logging.StreamHandler()

# Create and configure the Flask application
app = Flask(__name__)

# SQLite database path
db_path = os.getenv("DB_PATH")

# Initialize the Database object
db = Database(db_path)

# Initialize the MQTTClient object
mqtt_client = MQTTClient(os.getenv("MQTT_BROKER"), int(os.getenv("MQTT_PORT")), os.getenv("MQTT_TOPIC"), db)

# Route to display records on the web page
@app.route('/')
def index():
    name_filter = request.args.get('name_filter', '')
    rfid_filter = request.args.get('rfid_filter', '')
    
    # Retrieve records with applied filters
    records = db.get_records(name_filter=name_filter, rfid_filter=rfid_filter)
    
    return render_template('index.html', records=records)

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
