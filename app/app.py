import logging
import sqlite3
import uuid
import os
from logging.handlers import RotatingFileHandler

from flask import (Flask, jsonify, redirect, render_template, request)
from flask_swagger_ui import get_swaggerui_blueprint

# Creating the flask application
app = Flask(__name__)

log_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
log_file = 'app.log'
file_handler = RotatingFileHandler(
    log_file, maxBytes=1024 * 1024 * 100, backupCount=10)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# DATABASE = "birthdays.db"
app_dir = os.path.dirname(__file__)
db_path = os.path.join(app_dir, '..', 'data', 'birthdays.db')
DATABASE = db_path

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Birthday management Api"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


def get_birthdays_db():
    app.logger.debug('Connecting to the database')
    db_connection = sqlite3.connect(DATABASE)
    cursor = db_connection.cursor()
    cursor.execute("SELECT uuid, name, date FROM birthdays")
    columns = [column[0] for column in cursor.description]
    results = cursor.fetchall()
    birthdays = [dict(zip(columns, row)) for row in results]
    db_connection.close()
    app.logger.debug(f'Returned {len(birthdays)} birthdays')
    return birthdays


def get_single_birthdays_db(uuid):
    app.logger.debug(f"Getting birthday with UUID {uuid} from the database")
    db_connection = sqlite3.connect(DATABASE)
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT uuid, name, date FROM birthdays WHERE uuid = ?", (uuid,))
    columns = [column[0] for column in cursor.description]
    results = cursor.fetchall()
    birthdays = [dict(zip(columns, row)) for row in results]
    db_connection.close()
    app.logger.debug(f"Returned birthdays with UUID {uuid}")
    return birthdays


def insert_birthdays_db(birthday_data):
    app.logger.debug(
        f"Inserting new birthday into database with data: {birthday_data}")
    db_connection = sqlite3.connect(DATABASE)
    uuid_str = str(uuid.uuid4())
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO birthdays (uuid, name, date) VALUES(?,?,?)",
                   (uuid_str, birthday_data[0], birthday_data[1]))
    db_connection.commit()
    db_connection.close()
    app.logger.info(
        f"Added new birthday with name {birthday_data[0]} and date {birthday_data[1]} to database")
    return uuid_str


def del_birthdays_db(uuid):
    app.logger.debug(f"Deleting birthday with UUID {uuid} from the database")
    db_connection = sqlite3.connect(DATABASE)
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM birthdays WHERE uuid = ?", (uuid,))
    db_connection.commit()
    db_connection.close()


def put_birthdays_db(uuid, name=None, date=None):
    app.logger.debug(f"Updating birthday with UUID {uuid} in the database")
    db_connection = sqlite3.connect(DATABASE)
    cursor = db_connection.cursor()
    query = "UPDATE birthdays SET "
    if name:
        query += "name = ?, "
    if date:
        query += "date = ?, "
    query = query[:-2] + " WHERE uuid = ?"
    params = []
    if name:
        params.append(name)
    if date:
        params.append(date)
    params.append(uuid)
    cursor.execute(query, params)
    db_connection.commit()
    db_connection.close()


def check_existance_birthdays_db(uuid) -> bool:
    birthdays = get_single_birthdays_db(uuid)
    if len(birthdays) == 0:
        return False
    else:
        return True


def create_json_success_response(data, status_code):
    return jsonify({"data": data, "status": "success"}), status_code


def create_json_error_response(message, status_code):
    return jsonify({"message": message, "status": "error"}), status_code


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    app.logger.debug('Rendering index page')
    birthdays = get_birthdays_db()
    return render_template("index.html", birthdays=birthdays)


@app.route("/api/birthdays", methods=["GET", "POST"])
def get_or_post_birthdays():
    if request.method == "GET":
        birthdays = get_birthdays_db()
        return create_json_success_response(birthdays, 200)
    elif request.method == "POST":
        content_type = request.headers.get('Content-Type')
        data = []
        if content_type == 'application/x-www-form-urlencoded':
            data = request.form.get("name"), request.form.get("birthdate")
            insert_birthdays_db(data)
            return redirect("/")
        elif content_type == 'application/json':
            json_data = request.json
            data = json_data["name"], json_data["date"]
            uuid = insert_birthdays_db(data)
            json_data['uuid'] = uuid
            return create_json_success_response(json_data, 201)


@app.route("/api/birthdays/<uuid>", methods=["GET", "PUT", "DELETE"])
def update_or_delete_birthdays(uuid):
    uuid_exists = check_existance_birthdays_db(uuid)
    if request.method == "GET":
        birthday = get_single_birthdays_db(uuid)
        return create_json_success_response(birthday, 200)
    elif uuid_exists:
        if request.method == "PUT":
            jsonData = request.json
            name = jsonData.get('name')
            date = jsonData.get('date')
            put_birthdays_db(uuid, name, date)
            return create_json_success_response(jsonData, 200)
        elif request.method == "DELETE":
            del_birthdays_db(uuid)
            return create_json_success_response({'uuid': uuid}, 200)
    else:
        return create_json_error_response("UUID not found", 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
