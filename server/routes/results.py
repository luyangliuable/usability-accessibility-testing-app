from controllers.algorithm_data_controller import AlgorithmDataController
from download_parsers.gifdroid_json_parser import gifdroidJsonParser
from utility.safe_serialise import safe_serialize
from flask import Blueprint, request
from typing import TypeVar, Dict, Tuple
from flask_cors import cross_origin

# Initialise the blueprint
# Specifies the prefix for all routes in this file
results_blueprint = Blueprint('results', __name__, url_prefix='/results')

# Initialise the controller
algorithm_database_controller = AlgorithmDataController('apk', gifdroidJsonParser)


# Defines two routes for the blueprint, one where the algorithm is specified and one where it is not
@results_blueprint.route('/get/<uuid>', defaults={'algorithm': None},  methods=['GET'])
@results_blueprint.route('/get/<uuid>/<algorithm>',  methods=['GET'])
@cross_origin()
def get_result(uuid, algorithm=None):
    """

    Get the result of a given uuid and algorithm

    Path:
        /results/get/<uuid>             -> algorithm = None
        /results/get/<uuid>/<algorithm>
    Vars:
        uuid: The uuid of the result to get
        algorithm: The algorithm to get the result of


    TODO: Implement this method

    """

    print("uuid: ", str(uuid))
    print("algorithm: ", str(algorithm))

    if request.method == "GET":
        if algorithm is None:
            return safe_serialize(algorithm_database_controller.get(uuid)), 200
        else:
            return algorithm_database_controller._get_result_of_algorithm(uuid, algorithm), 200

    return "Failed", 500


# @results_blueprint.route('/add/<uuid>', defaults={'algorithm': None}, methods=['POST'])
@results_blueprint.route('/add/<uuid>/<algorithm>', methods=['POST'])
@cross_origin()
def add_result(uuid, algorithm=None):
    """

    Add a result to the database

    Path:
        /results/add/<uuid>             -> algorithm = None
        /results/add/<uuid>/<algorithm>
    Vars:
        uuid: The uuid of the result to add
        algorithm: The algorithm to add the result of
    Body:
        {
            "files": [str],
            "type": str,
            "names": [str]
        }

    TODO: Implement this method
    """

    print("uuid: " + uuid)
    print("algorithm: " + algorithm)

    if request.method == 'POST':
        links = request.json["files"]
        type = request.json["type"]
        file_names = request.json["names"]

        print("links: ", links)
        print("type: ", type)
        print("file_names: ", file_names)

        algorithm_database_controller._insert_algorithm_result(uuid, algorithm, links, type, file_names)

        return "Success", 200

    return "Fail", 500
