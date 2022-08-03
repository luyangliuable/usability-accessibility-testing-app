from flask import Flask
from flask import request
import os
import pymongo

from server.models.User import *

app = Flask(__name__)
try:
    mongo = pymongo.MongoClient("mongodb://username:password@localhost:27017/?authSource=admin")
    #mongo = pymongo.MongoClient("mongodb://localhost:27017/")
    
    db = mongo.users_db
    mongo.server_info()  # Triger exception if connection fails to the database
except Exception as ex:
    print('failed to connect', ex)


@app.route('/')
def home():
    return 'Flask with docker!'


@app.route('/signUp', methods=['POST'])
def signUpUser():
    return UserModel().signUpUser()


@app.route('/login', methods=['POST'])
def loginUser():
    return UserModel().loginUser()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
