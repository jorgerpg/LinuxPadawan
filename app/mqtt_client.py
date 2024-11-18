import json
import logging

import paho.mqtt.client as mqtt


class MQTTClient:
  def __init__(self, broker, port, topic, db):
    self.client = mqtt.Client()
    self.broker = broker
    self.port = port
    self.topic = topic
    self.topic_confirmation = topic + "/confirmation"
    self.db = db
    self.client.on_message = self.on_message
    self.client.connect(self.broker, self.port)
    self.start()
    logging.info("MQTTClient initialized")

  def start(self):
    """ Start the MQTT loop in a separate thread """
    self.client.subscribe(self.topic)
    logging.info(f"Client subd to topic {self.topic}")
    self.client.loop_start()

  def on_message(self, client, userdata, msg):
    """ Handle incoming MQTT messages """
    topic = msg.topic
    try:
      payload = msg.payload.decode()
      logging.info(f"Message received on topic {topic}: {payload}")

      # Parse the JSON payload
      data = json.loads(payload)
      rfid = data.get("rfid")

      if rfid:
        try:
          # Insert the data into the database
          self.db.insert_access(rfid)

          # Send a confirmation back to the ESP32
          confirmation = f"Access record for RFID {rfid} successfully created!"
          client.publish(self.topic_confirmation, confirmation)
        except Exception as e:
          logging.error(f"Failed to insert access record into database: {e}")
      else:
        logging.warning("Invalid data: 'rfid' is required")
    except json.JSONDecodeError as e:
      logging.error(f"Failed to decode JSON: {e}")
    except Exception as e:
      logging.error(f"Failed to process the access record: {e}")
