from controllers.algorithm_data_controller import AlgorithmDataController
from download_parsers.gifdroid_json_parser import gifdroidJsonParser
from utility.safe_serialise import safe_serialize
from flask import Blueprint, request
from typing import TypeVar, Dict, Tuple
from flask_cors import cross_origin


T = TypeVar('T')


###############################################################################
#                            Set Up Flask Blueprint                           #
###############################################################################
blueprint_name = "algorithm_datas"
algorithm_data_blueprint = Blueprint(blueprint_name, __name__)
algorithm_database_controller = AlgorithmDataController('apk', gifdroidJsonParser)


@algorithm_data_blueprint.route("/result/get/<uuid>/<algorithm>", methods=['GET'])
@cross_origin()
def get_result_of_algorithm(uuid: str, algorithm: str) -> Tuple[ Dict[str, str], int ]:
    """
    Method for getting a document from api
    """

    return algorithm_database_controller.get_result_of_algorithm(uuid, algorithm), 200


@algorithm_data_blueprint.route("/result/get/<uuid>", methods=['GET'])
@cross_origin()
def get_document(uuid) -> Tuple:
    """
    Method for getting a document from api
    """
    if request.method == "GET":
        return safe_serialize( algorithm_database_controller.get(uuid) ), 200

    return "Invalid request", 400


@algorithm_data_blueprint.route("/result/add/<uuid>/<algorithm>", methods=['GET', 'POST'])
@cross_origin()
def result_add(uuid, algorithm) -> Tuple[str, int]:
    """
    Method for adding result
    """
    if request.method == 'POST':
        links = request.json["files"]
        type = request.json["type"]
        file_names = request.json["names"]

        algorithm_database_controller.insert_algorithm_result(uuid, algorithm, links, type, file_names)

        return "Done", 200

    return "Invalid Request Type: "+request.method, 400


if __name__ == "__main__":
    pass
