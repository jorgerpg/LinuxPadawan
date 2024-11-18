import logging

from flask import Blueprint, jsonify, render_template, request
from sqlite import Database


def get_db_blueprint(db: Database):
  """
  Returns a Blueprint to manage routes.
  """
  db_bp = Blueprint("users", __name__)

  # Route to display records on the home page
  @db_bp.route('/')
  def index():
    name_filter = request.args.get('name_filter', '')
    rfid_filter = request.args.get('rfid_filter', '')

    # Retrieve records with the applied filters
    records = db.get_records(name_filter=name_filter, rfid_filter=rfid_filter)

    return render_template('index.html', records=records)

  @db_bp.route("/users", methods=["GET", "POST"])
  def manage_users():
    if request.method == 'POST':
      # Add new user
      name = request.form['name']
      rfid = request.form['rfid']
      try:
        db.add_user(name, rfid)
        success_message = "User added successfully!"
      except Exception as e:
        logging.error(f"Error adding user: {e}")
        return render_template("users.html", users=db.get_users(), error="Error adding user.")

    # Apply filters
    name_filter = request.args.get('name_filter', '').strip()
    rfid_filter = request.args.get('rfid_filter', '').strip()

    # Search for users in the database with the applied filters
    users = db.get_users(name_filter=name_filter, rfid_filter=rfid_filter)

    return render_template("users.html", users=users)

  @db_bp.route("/delete_user/<int:user_id>", methods=["POST"])
  def delete_user(user_id):
    try:
      db.delete_user(user_id)
      success_message = "User deleted successfully!"
      return render_template("users.html", users=db.get_users(), success=success_message)
    except Exception as e:
      logging.error(f"Error deleting user {user_id}: {e}")
      error_message = "Error deleting the user."
      return render_template("users.html", users=db.get_users(), error=error_message)

  return db_bp
