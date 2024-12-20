# database.py

import logging
import sqlite3
from datetime import datetime

import pytz


class Database:
  def __init__(self, db_path):
    self.db_path = db_path
    self.create_tables()
    logging.info("DB object initialized")

  def create_tables(self):
    """Ensure the necessary tables exist"""
    try:
      conn = self.connect()
      cursor = conn.cursor()

      # Criar tabela de usuários
      cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    rfid TEXT UNIQUE NOT NULL
                )
            """)

      # Criar tabela de registros de acesso
      cursor.execute("""
                CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    user_name TEXT NOT NULL,
                    status TEXT,
                    time TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)

      conn.commit()
      conn.close()
      logging.info("Tables 'users' and 'records' created or already exist.")
    except sqlite3.Error as e:
      logging.error(f"Error creating tables: {e}")

  def connect(self):
    """Connect to the SQLite database"""
    try:
      # Allow access from multiple threads
      conn = sqlite3.connect(self.db_path, check_same_thread=False)
      conn.row_factory = sqlite3.Row  # So we can access columns as dictionaries
      return conn
    except sqlite3.Error as e:
      logging.error(f"Error connecting to database: {e}")
      raise  # Reraise the exception after logging it

  def add_user(self, name, rfid):
    """Add a user to the 'users' table"""
    try:
      conn = self.connect()
      cursor = conn.cursor()
      cursor.execute(
          "INSERT INTO users (name, rfid) VALUES (?, ?)", (name, rfid))
      conn.commit()
      conn.close()
      logging.info(f"User {name} with RFID {rfid} successfully added.")
    except sqlite3.Error as e:
      logging.error(f"Error adding user to database: {e}")
      raise  # Reraise the exception after logging it

  def insert_access(self, rfid):
    """Insert an access record into the database with Granted or Denied status."""
    timezone = pytz.timezone("America/Sao_Paulo")
    time_now = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')

    try:
        conn = self.connect()
        cursor = conn.cursor()

        # Verificar se o RFID existe na tabela 'users'
        cursor.execute("SELECT id, name FROM users WHERE rfid = ?", (rfid,))
        user = cursor.fetchone()

        if user:
            user_id = user['id']
            user_name = user['name']
            status = "Granted"

            # Inserir o registro de acesso liberado
            cursor.execute(
                "INSERT INTO records (user_id, user_name, time, status) VALUES (?, ?, ?, ?)", 
                (user_id, user_name, time_now, status)
            )
            logging.info(
                f"Access record for {user_name} (RFID {rfid}) successfully inserted.")
        else:
            status = "Denied"

            # Inserir o registro de acesso negado
            cursor.execute(
                "INSERT INTO records (user_id, user_name, time, status) VALUES (?, ?, ?, ?)", 
                (None, "Unknown", time_now, status)
            )
            logging.warning(
                f"Access denied for unknown RFID {rfid}.")

        conn.commit()
        conn.close()
        return status
    except sqlite3.Error as e:
        logging.error(f"Error inserting access record into database: {e}")
        raise

  def get_records(self, name_filter='', rfid_filter=''):
    """Fetch access records from the database with optional filters"""
    try:
        conn = self.connect()
        cursor = conn.cursor()

        # Consultar a tabela records com a coluna status
        query = """
            SELECT id, user_name, time, status
            FROM records
            WHERE user_name LIKE ? AND time LIKE ?
            ORDER BY time DESC
        """
        cursor.execute(query, ('%' + name_filter + '%', '%' + rfid_filter + '%'))

        records = cursor.fetchall()
        conn.close()
        logging.info(f"Fetched {len(records)} records from the database.")
        return records
    except sqlite3.Error as e:
        logging.error(f"Error fetching records from database: {e}")
        return []

  def get_users(self, name_filter='', rfid_filter=''):
    """Fetch users from the database with optional filters"""
    try:
      conn = self.connect()
      cursor = conn.cursor()

      query = """
            SELECT *
            FROM users
            WHERE name LIKE ? AND rfid LIKE ?
            ORDER BY name ASC
        """

      cursor.execute(query, ('%' + name_filter + '%', '%' + rfid_filter + '%'))

      users = cursor.fetchall()
      conn.close()
      logging.info(f"Fetched {len(users)} users from the database.")
      return users
    except sqlite3.Error as e:
      logging.error(f"Error fetching users: {e}")
      return []

  def get_users_by_id(self, name_filter=''):
    """Fetch users from the database with optional filters"""
    try:
      conn = self.connect()
      cursor = conn.cursor()

      query = """
            SELECT *
            FROM users
            WHERE name LIKE ?
            ORDER BY name ASC
        """

      cursor.execute(query, ('%' + name_filter + '%'))

      users = cursor.fetchall()
      conn.close()
      logging.info(f"Fetched {len(users)} users from the database.")
      return users
    except sqlite3.Error as e:
      logging.error(f"Error fetching users: {e}")
      return []

  def delete_user(self, user_id):
    """Delete a user by ID"""
    try:
      conn = self.connect()
      cursor = conn.cursor()
      cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
      conn.commit()
      conn.close()
      logging.info(f"User with ID {user_id} successfully deleted.")
    except sqlite3.Error as e:
      logging.error(f"Error deleting user: {e}")
      raise
