import json
import logging

import paho.mqtt.client as mqtt


class MQTTClient:
  def __init__(self, broker, port, topic, db):
    self.client = mqtt.Client()
    self.broker = broker
    self.port = port
    self.topic_access = topic + "/access"
    self.topic_access_confirmation = self.topic_access + "/confirmation"
    self.topic_register_completed = topic + "/register/completed"
    self.db = db
    self.client.on_message = self.on_message
    self.client.connect(self.broker, self.port)
    self.start()
    logging.info("MQTTClient initialized")

  def start(self):
    """ Start the MQTT loop in a separate thread """
    self.client.subscribe(self.topic_access)
    self.client.subscribe(self.topic_register_completed)
    logging.info(
        f"Client subd to topics {self.topic_access} and {self.topic_register_completed}.")
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
        if topic == self.topic_access:
          try:
            # Insert the data into the database
            self.db.insert_access(rfid)
            # Send a granted confirmation back to the ESP32
            client.publish(self.topic_access_confirmation, "1")
          except Exception as e:
            # Send a denied confirmation back to the ESP32
            client.publish(self.topic_access_confirmation, "0")
            logging.error(f"Failed to insert access record into database: {e}")
        if topic == self.topic_register_completed:
          name = data.get("name")
          if name:
            try:
              self.db.add_user(name, rfid)
              success_message = "User added successfully!"
            except Exception as e:
              logging.error(f"Error adding user: {e}")
          else:
            logging.warning("Invalid data: 'name' is required for register.")
      else:
        logging.warning("Invalid data: 'rfid' is required")
    except json.JSONDecodeError as e:
      logging.error(f"Failed to decode JSON: {e}")
    except Exception as e:
      logging.error(f"Failed to process the access record: {e}")
