from flask import render_template, Blueprint, jsonify, request, Response, send_file, redirect, url_for
from flask_cors import cross_origin
from flask import Flask
import pymongo
import os

from models.User import *
from models.Report import ReportModel

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


@user_blueprint.route('/login', methods=['POST'])
@cross_origin()
def loginUser():
    if request.method == "POST":
        UserModel().signUpUser()
        return UserModel().loginUser()


@user_blueprint.route('/signup', methods=['POST'])
@cross_origin()
def signUpUser():
    if request.method == "POST":
        return UserModel().signUpUser()


@user_blueprint.route('/reports', methods=['POST'])
@cross_origin()
def getResults():
    print(request.json)
    if request.method == "POST":
        return ReportModel().getResults(request.json["user_id"])

if __name__ == "__main__":
    pass
    # login_blueprint.run(host="0.0.0.0", port=5002, debug=True)
