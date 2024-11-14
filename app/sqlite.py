# database.py

import sqlite3
from datetime import datetime
import logging

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_table()
        logging.info("DB object initialized")  # Exemplo de log

    def create_table(self):
        """ Ensure the table exists """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                rfid TEXT,
                time TEXT
            )
            """)
            conn.commit()
            conn.close()
            logging.info("Table 'records' created or already exists.")
        except sqlite3.Error as e:
            logging.error(f"Error creating table: {e}")

    def connect(self):
        """ Connect to the SQLite database """
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)  # Allow access from multiple threads
            conn.row_factory = sqlite3.Row  # So we can access columns as dictionaries
            return conn
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {e}")
            raise  # Reraise the exception after logging it

    def insert_access(self, name, rfid):
        """ Insert an access record into the database with transaction """
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Iniciar uma transação
            conn.isolation_level = None  # Utilizar o modo de autocommit
            cursor.execute("BEGIN TRANSACTION")

            # Inserir novo registro
            cursor.execute("INSERT INTO records (name, rfid, time) VALUES (?, ?, ?)", (name, rfid, time_now))
            
            # Finalizar a transação
            conn.commit()
            conn.close()
            logging.info(f"Access record for {name} with RFID {rfid} successfully inserted.")
        
        except sqlite3.Error as e:
            conn.rollback()  # Reverter qualquer mudança em caso de erro
            logging.error(f"Error inserting access record into database: {e}")
            raise  # Reraise the exception after logging it
        
    def get_records(self, name_filter='', rfid_filter=''):
        """ Fetch access records from the database with optional filters """
        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Criar a consulta com filtros opcionais
            query = "SELECT * FROM records WHERE name LIKE ? AND rfid LIKE ? ORDER BY time DESC"
            cursor.execute(query, ('%' + name_filter + '%', '%' + rfid_filter + '%'))

            records = cursor.fetchall()
            conn.close()
            logging.info(f"Fetched {len(records)} records from the database.")
            return records
        except sqlite3.Error as e:
            logging.error(f"Error fetching records from database: {e}")
            return []  # Return an empty list in case of an error