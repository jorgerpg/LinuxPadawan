# Padawan Program - Linux Project for Access Control with ESP32 and MQTT

This repository contains the Linux component of the **Internal Electronics Training Completion Project** at **CIMATEC**, called the **Padawan Program**. The project's goal is to develop an access control system that uses the ESP32 as a microcontroller, a Python container to process access information, and MQTT communication to exchange data between devices.

## Project Description

This system allows access control to a specific area using the ESP32, which is configured to send data via **MQTT** protocol to a Python application running on Linux. Upon receiving the RFID identifier, the application logs the access in the database and provides confirmation feedback to the ESP32.

### Components

1. **ESP32** - Microcontroller that manages access via RFID and communicates via MQTT.
2. **Linux Server with Docker** - Platform hosting the project's Docker containers.
3. **Mosquitto MQTT Broker** - MQTT broker responsible for mediating communication between the ESP32 and the Python application.
4. **Python Application** - Service that processes received MQTT messages, logs access in the SQLite database, and provides confirmation.

## Project Structure

The project is structured into Docker containers, each fulfilling a specific role in the system:

- **Python Application**: Consumes messages from the MQTT broker and inserts records into the database.
- **Mosquitto MQTT Broker**: Communication channel for message exchange between the ESP32 and the Python container.
- **SQLite Database**: Stores access records, which can be queried and filtered via the web application.

## Prerequisites

- **Docker** and **Docker Compose**
- ESP32 configured for MQTT communication
- MQTT client for testing and message validation

## Project Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your_username/padawan_project.git
    cd padawan_project
    ```

2. **Configure Docker Compose**:
   Make sure the `docker-compose.yml` file is correctly configured with the necessary environment variables for each container.

3. **Start the Containers**:
    ```bash
    docker-compose up --build
    ```

   This command will create and start the containers for Mosquitto and the Python application.

## Operation

1. **ESP32 Configuration**: The ESP32 is configured to send MQTT messages containing the user's name and RFID to the broker.
2. **Message Processing**: The Python application listens to the specified MQTT topic (`lock/access`) and processes the messages in JSON format.
3. **Database Logging**: Each access is recorded in an SQLite database with name and RFID data.
4. **Feedback to ESP32**: After logging, a confirmation message is sent back to the ESP32.

## Web Interface

The system includes a basic web interface where access records are displayed. The main page allows filtering by name and RFID, facilitating data lookup.

## File Structure

- `app.py`: Flask server for the web interface and system initialization.
- `mqtt_client.py`: Class for MQTT communication with the ESP32.
- `sqlite.py`: Class for managing the SQLite database.
- `docker-compose.yml`: Docker Compose configuration file.
- `requirements.txt`: Python project dependencies.

## Usage Examples

1. **Send MQTT Message with JSON**:
   ```json
   {
       "name": "John Doe",
       "rfid": "1234567890"
   }
   ```

2. **Query Records in the Web Interface**:
   - Open your browser and go to: `http://localhost:5000`
   - Use the filters to search specific records by name or RFID.
