import logging
import os

from flask import Flask
from mqtt_client import MQTTClient
from routes.db_bp import get_db_blueprint
from sqlite import Database

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
mqtt_client = MQTTClient(os.getenv("MQTT_BROKER"), int(
    os.getenv("MQTT_PORT")), os.getenv("MQTT_TOPIC"), db)

# Registrar o Blueprint
app.register_blueprint(get_db_blueprint(db))

# Start the Flask server
if __name__ == "__main__":
  app.run(debug=False, host='0.0.0.0', port=5000)
