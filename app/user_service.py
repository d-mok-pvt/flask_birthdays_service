import sqlite3
import uuid

from flask import Blueprint, request
from flask_restx import Api, Resource, fields, Namespace
from werkzeug.security import generate_password_hash

from config import DATABASE

user_service = Blueprint('user_service', __name__)
api = Api(user_service, version='1.0', title='User Management API',
          description='API for managing users and their passwords',
          tags=[{'name': 'User Management', 'description': 'Operations related to user management'}])

user_ns = Namespace('User Management', description='Operations related to user management')
api.add_namespace(user_ns, path = '/users')

user_model = user_ns.model('User', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password')
})

password_model = user_ns.model('Password', {
    'new_password': fields.String(required=True, description='The new password')
})

def create_user(username, password):
    db_connection = sqlite3.connect(DATABASE)
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    if cursor.fetchone()[0] > 0:
        db_connection.close()
        return None
    hashed_password = generate_password_hash(password)
    userid = str(uuid.uuid4())
    cursor.execute("INSERT INTO users (userid, username, password) VALUES (?, ?, ?)",
                   (userid, username, hashed_password))
    db_connection.commit()
    db_connection.close()
    return userid


def delete_user(userid):
    db_connection = sqlite3.connect(DATABASE)
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM users WHERE userid = ?", (userid,))
    if cursor.rowcount == 0:
        db_connection.close()
        return False
    db_connection.commit()
    db_connection.close()
    return True


def change_password(userid, new_password):
    db_connection = sqlite3.connect(DATABASE)
    cursor = db_connection.cursor()
    hashed_password = generate_password_hash(new_password)
    cursor.execute("UPDATE users SET password = ? WHERE userid = ?", (hashed_password, userid))
    if cursor.rowcount == 0:
        db_connection.close()
        return False
    db_connection.commit()
    db_connection.close()
    return True


@user_ns.route('/user')
class UserList(Resource):
    @user_ns.expect(user_model)
    @user_ns.response(201, 'User created successfully')
    @user_ns.response(400, 'Validation Error')
    def post(self):
        json_data = request.json
        username = json_data.get("username")
        password = json_data.get("password")
        if not username or not password:
            return {"message": "Username and password are required", "status": "error"}, 400
        userid = create_user(username, password)
        if userid:
            return {"data": {"userid": userid}, "status": "success"}, 201
        else:
            return {"message": "User already exists", "status": "error"}, 419


@user_ns.route('/<userid>')
class User(Resource):
    @user_ns.response(200, 'User deleted successfully')
    @user_ns.response(404, 'User not found')
    def delete(self, userid):
        if not delete_user(userid):
            return {"message": "User not found", "status": "error"}, 404
        return {"data": {"userid": userid}, "status": "success"}, 200


@user_ns.route('/<userid>/password')
class UserPassword(Resource):
    @user_ns.expect(password_model)
    @user_ns.response(200, 'Password changed successfully')
    @user_ns.response(400, 'Validation Error')
    @user_ns.response(404, 'User not found')
    def put(self, userid):
        json_data = request.json
        new_password = json_data.get("new_password")
        if not new_password:
            return {"message": "New password is required", "status": "error"}, 400
        if not change_password(userid, new_password):
            return {"message": "User not found", "status": "error"}, 404
        return {"data": {"userid": userid}, "status": "success"}, 200
