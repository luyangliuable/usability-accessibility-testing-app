from flask import render_template, Blueprint, jsonify, request, Response, send_file, redirect, url_for
from flask_cors import cross_origin
from flask import Flask
import pymongo
import os

from models.User import *

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/signUp', methods=['POST'])
@cross_origin()
def signUpUser():
    if request.method == "POST":
        return UserModel().signUpUser()


@login_blueprint.route('/login', methods=['POST', 'GET'])
@cross_origin()
def loginUser():
    if request.method == "POST":
        return UserModel().loginUser()
    if request.method == "GET":
        return getUserCollectionJSON()


if __name__ == "__main__":
    pass
    # login_blueprint.run(host="0.0.0.0", port=5002, debug=True)
