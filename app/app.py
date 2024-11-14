import os
from flask import Flask, render_template, request
from sqlite import Database
from mqtt_client import MQTTClient
import logging

# Configuração básica do logging para enviar tudo ao stdout
logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(levelname)s - %(message)s'
)
handler = logging.StreamHandler()

# Criar e configurar o aplicativo Flask
app = Flask(__name__)

# Caminho do banco de dados SQLite
db_path = os.getenv("DB_PATH")

# Inicializar o objeto Database
db = Database(db_path)

# Inicializar o objeto MQTTClient
mqtt_client = MQTTClient(os.getenv("MQTT_BROKER"), int(os.getenv("MQTT_PORT")), os.getenv("MQTT_TOPIC"), db)

# Rota para exibir os registros na página web
@app.route('/')
def index():
    name_filter = request.args.get('name_filter', '')
    rfid_filter = request.args.get('rfid_filter', '')
    
    # Obter os registros com os filtros aplicados
    records = db.get_records(name_filter=name_filter, rfid_filter=rfid_filter)
    
    return render_template('index.html', records=records)

# Iniciar o servidor Flask
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
