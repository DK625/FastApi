import json
from datetime import datetime, timedelta

import jwt
from flask import Flask, current_app, jsonify, request

from ..config.connect_db import db
from ..config.marsh_mallow import user_schema
from ..controllers.verify_and_authorization import Middleware
from ..models.model import User
from ..services import user_service

users_schema = user_schema(many=True)


def sign_up():
    data = json.loads(request.data)
    if data and ("name" in data) and ("email" in data) and ("password" in data) and ("comfirm_password" in data):
        name = data["name"]
        email = data["email"]
        password = data["password"]
        confirm_password = data["comfirm_password"]
        user_data = user_service.handle_user_sign_up(name, email, password, confirm_password)
        response = jsonify(
            {
                "err_code": user_data["err_code"],
                "message": user_data["err_message"],
            }
        )
        response.status_code = 200
        return response
    response = jsonify(
        {
            "err_code": "1",
            "message": "Missing inputs parameter!",
        }
    )
    response.status_code = 404
    return response


def handle_loging():
    data = json.loads(request.data)
    if data and ("email" in data) and ("password" in data):
        email = data["email"]
        password = data["password"]
        user_data = user_service.handle_user_login(email, password)
        if user_data["err_code"] == 0:
            token = jwt.encode(
                {
                    "email": email,
                    "exp": datetime.utcnow() + timedelta(minutes=30000),
                },
                current_app.config["SECRET_KEY"],
            )
            response = jsonify(
                {
                    "token": token,
                    "err_code": user_data["err_code"],
                    "err_message": user_data["err_message"],
                }
            )
            response.status_code = 200
            return response
        response = jsonify(
            {
                "err_code": user_data["err_code"],
                "message": user_data["err_message"],
            }
        )
        response.status_code = 200
        return response
    response = jsonify({"err_code": "1", "message": "Missing inputs parameter!"})
    response.status_code = 404
    return response


def create_new_list():
    data = json.loads(request.data)
    try:
        current_user = Middleware()
        user_data = user_service.create_new_list(data, current_user["email"])
        return jsonify(
            {
                "message": user_data,
            }
        )
    except:
        return jsonify(
            {
                "err_message": "not logged in yet",
            }
        )


def create_new_todo():
    data = json.loads(request.data)

    try:
        current_user = Middleware()
        user_data = user_service.create_new_todo(data, current_user["email"])
        return jsonify(
            {
                "message": user_data,
            }
        )
    except:
        return jsonify(
            {
                "err_message": "not logged in yet",
            }
        )


def get_todo_list():
    try:
        data = Middleware()
        if data and ("email" in data):
            user_data = user_service.get_list(data)
            return jsonify({"err_code": 0, "err_message": "OK", "lists to do": user_data})
        return jsonify({"err_code": "1", "err_message": "Missing inputs parameter!"})
    except:
        return jsonify({"err_message": "not logged in yet"})


def get_todo():
    data = json.loads(request.data)
    try:
        current_user = Middleware()
        user_data = user_service.get_todo(data, current_user["email"])
        return jsonify({"err_code": 0, "err_message": "OK", "todos": user_data})
    except:
        return jsonify({"err_message": "not logged in yet"})


def delete_list():
    try:
        current_user = Middleware()
        data = json.loads(request.data)
        if data and "list_name" in data:
            message = user_service.delete_list(data["list_name"], current_user["email"])
            response = jsonify({"message": message})
            response.status_code = 202
            return response
        return jsonify({"err_code": "1", "err_message": "Missing inputs parameter!"})
    except:
        return jsonify({"err_message": "not logged in yet"})


def delete_todo():
    try:
        current_user = Middleware()
        data = json.loads(request.data)
        if data and "title" in data:
            message = user_service.delete_todo(data["title"], current_user["email"])
            response = jsonify({"message": message})
            response.status_code = 202
            return response
        return jsonify({"err_code": "1", "err_message": "Missing inputs parameter!"})
    except:
        return jsonify({"err_message": "not logged in yet"})


def update_todo():
    current_user = Middleware()
    data = json.loads(request.data)
    if data and ("title" in data) and ("status" in data):
        message = user_service.update_todo(data["title"], data["status"], current_user["email"])
        response = jsonify({"message": message})
        response.status_code = 202
        return response
    return jsonify({"err_code": "1", "err_message": "Missing inputs parameter!"})


# try:
#     current_user = Middleware()
#     data = json.loads(request.data)
#     if data and ("title" in data) and ("status" in data):
#         message = user_service.update_todo(data["title"], data["status"], current_user["email"])
#         response = jsonify({"message": message})
#         response.status_code = 202
#         return response
#     return jsonify({"err_code": "1", "err_message": "Missing inputs parameter!"})
# except:
#     return jsonify({"err_message": "not logged in yet"})
