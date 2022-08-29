import base64
from flask import Flask, jsonify, request
import uuid
import json

from models.DBManager import DBManager


def getUserCollection():
    mongo = DBManager.instance()

    users = mongo.get_collection('users')
    if users is None:
        mongo.create_collection('users')
        users = mongo.get_collection('users')

    return users


class UserModel:
    def signUpUser(self):
        json_response = request.json
        users = getUserCollection()

        new_user = {
            "id": str(uuid.uuid4()),
            "email": json_response["email"],
            "password": base64.b64encode(json_response["password"].encode("utf-8"))
        }

        if users is None:
            return json.dumps({"ERROR": "Could not load users DB collection"}), 500

        # Checking is user with email already exists
        print('\n\n')
        print(users.find_one({"email": new_user["email"]}))
        print('\n\n')

        if users.find_one({"email": new_user["email"]}):
            return json.dumps({"ERROR": "A user with this email already exists"}), 400

        # If all the checks are passed , insert user into database
        users.insert_one(new_user)
        return json.dumps({"Success": "User successfully signed up", "user_id": new_user["id"]}), 200

    def loginUser(self):
        json_response = request.json
        users = getUserCollection()

        if users is None:
            return json.dumps({"ERROR": "Could not load users DB collection"}), 500

        inst = users.find_one({"email": json_response["email"]})

        if inst and inst["password"] == base64.b64encode(json_response["password"].encode("utf-8")):
            return json.dumps({"Success": "User successfully logged in", "user_id": inst["id"]}), 200

        return json.dumps({"ERROR": "Couldn't find user in database or invalid login details"}), 400
