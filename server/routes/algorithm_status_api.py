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
asc = algorithm_status_controller(default_collection)

@algorithm_status_blueprint.route("/status/get/<uuid>", methods=['GET'])
@cross_origin()
def get_status(uuid):
    """
    Method for getting a status of each and every algorithm
    """

    res = asc.get_algorithm_status(uuid)

    return json.dumps(res)


@algorithm_status_blueprint.route("/status/update/<uuid>", methods=['GET', 'POST'])
@cross_origin()
def update_status(uuid):
    """
    Method for updating status of each and every algorithm
    """
    if request.method == "POST":
        update = request.json

        res = asc.update_algorithm_status(uuid, update)
        return json.dumps(res), 200

@algorithm_status_blueprint.route("/status/update/<uuid>/<algorithm>", methods=['GET', 'POST'])
@cross_origin()
def update_one_algorithm(uuid, algorithm):
    """
    Method for updating status of each and every algorithm
    """
    pass


@algorithm_status_blueprint.route("/status/update/<uuid>/<algorithm>/<attribute>", methods=['GET', 'POST'])
@cross_origin()
def update_one_attribute(uuid, algorithm, attribute):
    """
    Method for updating status of each and every algorithm
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
    pass


@algorithm_status_blueprint.route("/status/update", methods=['GET'])
@cross_origin()
def u_status():
    pass


@algorithm_status_blueprint.route("/status/get", methods=['GET'])
@cross_origin()
def g_status():
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
