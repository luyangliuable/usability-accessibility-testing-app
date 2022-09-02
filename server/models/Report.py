import base64
from flask import Flask, jsonify, request
import json
from models.DBManager import DBManager

from bson import json_util


def getReportCollection():
    mongo = DBManager.instance()

    reports = mongo.get_collection('reports')
    if reports is None:
        mongo.create_collection('reports')
        reports = mongo.get_collection('reports')

    return reports


class ReportModel:

    def uploadResult(self):
        json_response = request.json
        reports = getReportCollection()

        if reports is None:
            return json.dumps({"ERROR": "Could not load reports DB collection"}), 500

        new_report = {
            "user_id": json_response["user_id"],
            "result_id": json_response["result_id"]
        }

        try:
            reports.insert_one(new_report)
            return json.dumps({"Success": "Report successfully created"}), 200
        except:
            return json.dumps({"ERROR": "Failed to create report"}), 500

    def getResults(self):
        json_response = request.json
        reports = getReportCollection()

        if reports is None:
            return json.dumps({"ERROR": "Could not load reports DB collection"}), 500

        results = reports.find({"user_id": json_response["user_id"]})
        print(results)

        return json_util.dumps({"user_id": json_response["user_id"], "results": list(results)}), 200
