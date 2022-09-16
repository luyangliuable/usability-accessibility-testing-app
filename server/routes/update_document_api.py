from flask import Blueprint, request, jsonify
from controllers.update_document_controller import UpdateDocumentController
from download_parsers.gifdroid_json_parser import gifdroidJsonParser
from flask_cors import cross_origin
from utility.safe_serialise import safe_serialize
from utility.uuid_generator import unique_id_generator
import requests
from typing import TypeVar, Generic, List, Callable, Dict, Tuple


T = TypeVar('T')


###############################################################################
#                            Set Up Flask Blueprint                           #
###############################################################################
update_document_blueprint = Blueprint("file", __name__)
file_controller = UpdateDocumentController('apk', gifdroidJsonParser)


@update_document_blueprint.route("/result/get/<uuid>/<algorithm>", methods=['GET'])
@cross_origin()
def get_result_of_algorithm(uuid: str, algorithm: str) -> Tuple[ Dict[str, str], int ]:
    """
    Method for getting a document from api
    """

    return file_controller.get_result_of_algorithm(uuid, algorithm), 200


@update_document_blueprint.route("/result/get/<uuid>", methods=['GET'])
@cross_origin()
def get_document(uuid) -> Tuple:
    """
    Method for getting a document from api
    """
    if request.method == "GET":
        return safe_serialize( file_controller.get_document(uuid) ), 200

    return "Invalid request", 400


@update_document_blueprint.route("/result/add/<uuid>/<algorithm>", methods=['GET', 'POST'])
@cross_origin()
def result_add(uuid, algorithm) -> Tuple[str, int]:
    """
    Method for adding result
    """
    if request.method == 'POST':
        links = request.json["files"]
        type = request.json["type"]
        file_names = request.json["names"]

        file_controller.insert_algorithm_result(uuid, algorithm, links, type, file_names)

        return "Done", 200

    return "Invalid Request Type: "+request.method, 400


if __name__ == "__main__":
    pass
