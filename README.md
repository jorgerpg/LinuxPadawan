# Padawan Program - Linux Project for Access Control with ESP32 and MQTT

This repository contains the Linux component of the **Internal Electronics Training Completion Project** at **CIMATEC**, called the **Padawan Program**. The project's goal is to develop an access control system that uses the ESP32 as a microcontroller, a Python container to process access information, and MQTT communication to exchange data between devices.

## Project Description

This system allows access control to a specific area using the ESP32, which is configured to send data via **MQTT** protocol to a Python application running on Linux. Upon receiving the RFID identifier, the application logs the access in the database, validates if the RFID is registered, and provides confirmation feedback to the ESP32.

### Components

1. **ESP32** - Microcontroller that manages access via RFID and communicates via MQTT.
2. **Linux Server with Docker** - Platform hosting the project's Docker containers.
3. **Mosquitto MQTT Broker** - MQTT broker responsible for mediating communication between the ESP32 and the Python application.
4. **Python Application** - Service that processes received MQTT messages, logs access in the SQLite database, validates registered users, and provides confirmation.
5. **SQLite Database** - Stores access records, including user information such as RFID and name.

## Project Structure

The project is structured into Docker containers, each fulfilling a specific role in the system:

- **Python Application**: Consumes messages from the MQTT broker, validates RFID data against the user database, logs records, and provides feedback.
- **Mosquitto MQTT Broker**: Communication channel for message exchange between the ESP32 and the Python container.
- **SQLite Database**: Stores user records, including name and RFID, and access logs.

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
2. **User Registration**: Users can be registered through a web interface or via API by sending the user's name and RFID to the Python application, which stores the details in the SQLite database.
3. **Message Processing**: The Python application listens to the specified MQTT topic (`lock/access`) and processes the messages in JSON format. When a message with an RFID is received, it checks if the RFID exists in the database.
4. **Database Logging**: If the RFID exists in the database, the access is logged with the user's name and RFID. If the RFID is not found, a rejection message is sent to the ESP32.
5. **Feedback to ESP32**: After validating the RFID and logging the access, a confirmation message is sent back to the ESP32. If the RFID is invalid, the feedback indicates that the access is denied.

## Web Interface

The system includes a basic web interface where access records are displayed, and users can be registered. The main page allows filtering by name and RFID, facilitating data lookup. Additionally, there is a page for user registration where RFID and names can be added.

## File Structure

- `app.py`: Flask server for the web interface, user registration, and system initialization.
- `mqtt_client.py`: Class for MQTT communication with the ESP32.
- `sqlite.py`: Class for managing the SQLite database and user records.
- `docker-compose.yml`: Docker Compose configuration file.
- `requirements.txt`: Python project dependencies.

## Usage Examples

1. **Send MQTT Message with JSON**:
   ```json
   {
       "rfid": "1234567890"
   }
   ```

2. **Query Records in the Web Interface**:
   - Open your browser and go to: `http://localhost:5000`
   - Use the filters to search specific records by name or RFID.

3. **Register a New User**:
   - Open the user registration page on `http://localhost:5000/register`
   - Provide the user's name and RFID to register them in the system.

---