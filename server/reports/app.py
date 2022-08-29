from flask import Flask
from flask import render_template, Blueprint, jsonify, request, Response, send_file, redirect, url_for
from flask_cors import cross_origin


import os
import pymongo

from models.Report import *

reports_blueprint = Blueprint('reports', __name__)


@reports_blueprint.route('/create_result', methods=['POST'])
@cross_origin()
def createResult():
    print(request.json)
    if request.method == "POST":
        return ReportModel().uploadResult()


@reports_blueprint.route('/get_results', methods=['POST'])
@cross_origin()
def getResults():
    print(request.json)
    if request.method == "POST":
        return ReportModel().getResults()


if __name__ == "__main__":
    pass
    # login_blueprint.run(host="0.0.0.0", port=5002, debug=True)
