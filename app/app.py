import base64
import logging
import sqlite3
import uuid
from logging.handlers import RotatingFileHandler

from flask import (Flask, jsonify, redirect, render_template, request)
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.datastructures import MultiDict
from werkzeug.security import check_password_hash

from config import DATABASE
from config import default_userid
from forms import AddBirthdayForm, UpdateBirthdayForm
from user_service import user_service

# Creating the flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['WTF_CSRF_ENABLED'] = False
CORS(app)

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

SWAGGER_URL = '/api/swagger-ui'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Birthday management Api"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
app.register_blueprint(user_service, url_prefix='/api/internal/admin')


# Function to fetch users from the database
def fetch_users():
    db_connection = sqlite3.connect(DATABASE)
    cursor = db_connection.cursor()
    cursor.execute("SELECT userid, username, password FROM users")
    users = {row[1]: {'userid': row[0], 'password': row[2]} for row in cursor.fetchall()}
    db_connection.close()
    return users


# Initialize HTTPBasicAuth
auth = HTTPBasicAuth()

def check_auth(request_to_check):
    auth_header = request_to_check.headers.get('Authorization')
    if auth_header:
        auth_type, auth_credentials = auth_header.split(None, 1)
        if auth_type.lower() == 'basic':
            username, password = base64.b64decode(auth_credentials).decode('utf-8').split(':', 1)
            userid = verify_password(username, password)
            if userid:
                return userid
            else:
                return None


def verify_password(username, password):
    users = fetch_users()
    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        return user['userid']
    return None


def get_birthdays_db(userid):
    app.logger.debug('Connecting to the database')
    db_connection = sqlite3.connect(DATABASE)
    cursor = db_connection.cursor()
    cursor.execute("SELECT uuid, name, date FROM birthdays where userid = ?", (userid,))
    columns = [column[0] for column in cursor.description]
    results = cursor.fetchall()
    birthdays = [dict(zip(columns, row)) for row in results]
    db_connection.close()
    app.logger.debug(f'Returned {len(birthdays)} birthdays')
    return birthdays


def get_single_birthdays_db(userid, uuid):
    app.logger.debug(f"Getting birthday for user {userid} with UUID {uuid} from the database")
    db_connection = sqlite3.connect(DATABASE)
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT userid, uuid, name, date FROM birthdays WHERE userid = ? and uuid = ?", (userid, uuid,))
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
    cursor.execute("INSERT INTO birthdays (userid, uuid, name, date) VALUES(?,?,?,?)",
                   (birthday_data[0], uuid_str, birthday_data[1], birthday_data[2]))
    db_connection.commit()
    db_connection.close()
    app.logger.info(
        f"Added new birthday for user {birthday_data[0]} with name {birthday_data[1]} and date {birthday_data[2]} to database")
    return uuid_str


def del_birthdays_db(userid, uuid):
    app.logger.debug(f"Deleting birthday of user {userid} with UUID {uuid} from the database")
    db_connection = sqlite3.connect(DATABASE)
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM birthdays WHERE userid = ? AND uuid = ?", (userid, uuid,))
    db_connection.commit()
    db_connection.close()


def put_birthdays_db(userid, uuid, name=None, date=None):
    app.logger.debug(f"Updating birthday of user {userid} with UUID {uuid} in the database")
    db_connection = sqlite3.connect(DATABASE)
    cursor = db_connection.cursor()
    query = "UPDATE birthdays SET "
    if name:
        query += "name = ?, "
    if date:
        query += "date = ?, "
    query = query[:-2] + " WHERE userid = ? and uuid = ?"
    params = []
    if name:
        params.append(name)
    if date:
        params.append(date)
    params.append(userid)
    params.append(uuid)
    cursor.execute(query, params)
    db_connection.commit()
    db_connection.close()


def check_existance_birthdays_db(userid, uuid) -> bool:
    birthdays = get_single_birthdays_db(userid, uuid)
    if len(birthdays) == 0:
        return False
    else:
        return True


def create_json_success_response(data, status_code):
    return jsonify({"data": data, "status": "success"}), status_code


def create_json_error_response(message, status_code):
    return jsonify({"message": message, "status": "error"}), status_code


def create_json_error_response_with_data(message, data, status_code):
    return jsonify({"message": message, "data": data, "status": "error"}), status_code


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    app.logger.debug('Rendering index page')
    birthdays = get_birthdays_db(default_userid)
    return render_template("index.html", birthdays=birthdays)


@app.route("/api/birthdays", methods=["GET", "POST"])
def get_or_post_birthdays():
    content_type = request.headers.get('Content-Type')
    if request.method == "GET":
        if content_type == 'application/x-www-form-urlencoded':
            birthdays = get_birthdays_db(default_userid)
            return create_json_success_response(birthdays, 200)
        elif request.headers.get('accept') == 'application/json' or content_type == 'application/json':
            userid = check_auth(request)
            if userid:
                birthdays = get_birthdays_db(userid)
                return create_json_success_response(birthdays, 200)
            else:
                return create_json_error_response("Unauthorized", 401)
    elif request.method == "POST":
        if content_type == 'application/x-www-form-urlencoded':
            data = default_userid, request.form.get("name"), request.form.get("birthdate")
            insert_birthdays_db(data)
            return redirect("/")
        elif content_type == 'application/json':
            userid = check_auth(request)
            if userid:
                json_data = request.json
                form_data = MultiDict(json_data)
                form = AddBirthdayForm(form_data)
                if form.validate():
                    data = userid, json_data["name"], json_data["date"]
                    uuid = insert_birthdays_db(data)
                    json_data['uuid'] = uuid
                    return create_json_success_response(json_data, 201)
                else:
                    return create_json_error_response_with_data("Invalid request parameters", form.errors, 400)
            else:
                return create_json_error_response("Unauthorized", 401)


@app.route("/api/birthdays/<uuid>", methods=["GET", "PUT", "DELETE"])
def update_or_delete_birthdays(uuid):
    userid = check_auth(request)
    uuid_exists = check_existance_birthdays_db(userid, uuid)
    if userid:
        if uuid_exists:
            if request.method == "GET":
                birthday = get_single_birthdays_db(userid, uuid)[0]
                return create_json_success_response(birthday, 200)
            elif request.method == "PUT":
                json_data = request.json
                form_data = MultiDict(json_data)
                form = UpdateBirthdayForm(form_data)
                if form.validate():
                    name = json_data.get('name')
                    date = json_data.get('date')
                    put_birthdays_db(userid, uuid, name, date)
                    return create_json_success_response(json_data, 200)
                else:
                    return create_json_error_response_with_data(
                        "Invalid request parameters", "At least one of 'name' or 'date' is required.", 400)
            elif request.method == "DELETE":
                del_birthdays_db(userid, uuid)
                return create_json_success_response({'uuid': uuid}, 200)
        else:
            return create_json_error_response("UUID not found", 404)
    else:
        return create_json_error_response("Unauthorized", 401)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
