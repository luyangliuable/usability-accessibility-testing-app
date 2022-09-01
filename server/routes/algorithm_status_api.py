from botocore.exceptions import requests
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import datetime
import requests
import json
import uuid
from controllers.algorithm_status_controller import *

###############################################################################
#                            Set Up Flask Blueprint                           #
###############################################################################
algorithm_status_blueprint = Blueprint("algorithm_status", __name__)

###############################################################################
#                Initiate algorithm status controller for route               #
###############################################################################
default_collection = 'apk'
asc = AlgorithmStatusController(default_collection)


@algorithm_status_blueprint.route("/status/get/<uuid>", methods=['GET'])
@cross_origin()
def get_job_status(uuid):
    """
    Method for getting a status of each and every algorithm
    """
    if request.method == "GET":

    res = asc.get_job_status(uuid)

    print(res)

    return json.dumps(res), 200


@algorithm_status_blueprint.route("/status/update/<uuid>/<algorithm>", methods=['GET', 'POST'])
@cross_origin()
def update_algorthm_status(uuid, algorithm):
    """
    Method for updating status of each and every algorithm
    """
    if request.method == "POST":
        status = str( request.data.decode() )

        res = asc.update_algorithm_status(uuid, algorithm, status)
        return json.dumps(res), 200


@algorithm_status_blueprint.route("/status/update/<uuid>", methods=['GET', 'POST'])
@cross_origin()
def update_job_status(uuid):
    """
    Method for updating status of each and every algorithm
    """
    if request.method == "POST":
        status = str( request.data.decode() )

        res = asc.update_job_status(uuid, status)
        return json.dumps(res), 200


@algorithm_status_blueprint.route("/status/get/<uuid>/<algorithm>", methods=['GET'])
@cross_origin()
def get_one_algorithm_status(uuid, algorithm):
    """
    Method for updating status of each and every algorithm
    """
    if request.method == "GET":

        res = asc.get_specific_algorithm_status(uuid, algorithm)

        return json.dumps(res), 200
    else:
        return request.method + " not valid", 400


@algorithm_status_blueprint.route("/status/update/<uuid>/<algorithm>", methods=['GET', 'POST'])
@cross_origin()
def update_one_algorithm_status(uuid, algorithm):
    """
    Method for updating status of each and every algorithm
    """
    if request.method == "POST":
        status = str( request.data.decode() )

        res = asc.update_algorithm_status(uuid, algorithm, status)

        return json.dumps(res), 200
    else:
        return request.method + " not valid", 400


@algorithm_status_blueprint.route("/status/update/<uuid>/<algorithm>/<attribute>", methods=['GET', 'POST'])
@cross_origin()
def update_one_attribute_in_status(uuid, algorithm, attribute):
    """
    Method for updating one attribute inside status of each and every algorithm
    """
    if request.method == "POST":
        # Assume result is a string
        update = str( request.data.decode() )

        res = asc.update_algorithm_status_attribute(uuid, algorithm, attribute, update)

        print(res)

        return safe_serialize( res ), 200


@algorithm_status_blueprint.route("/status", methods=['GET'])
@cross_origin()
def status():
    "Status getter is online", 200


@algorithm_status_blueprint.route("/status/update", methods=['GET'])
@cross_origin()
def u_status():
    pass


###############################################################################
#                              Utility Functions                              #
###############################################################################
def safe_serialize(obj):
    default = lambda o: f"<<non-serializable: {type(o).__qualname__}>>"
    return json.dumps(obj, default=default)


def unique_id_generator():
    res = str( uuid.uuid4() )
    return res


if __name__ == "__main__":
    pass
