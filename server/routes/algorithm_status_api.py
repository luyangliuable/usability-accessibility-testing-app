from utility.uuid_generator import unique_id_generator
from controllers.algorithm_status_controller import *
from utility.safe_serialise import safe_serialize
from flask import Blueprint, request
from flask_cors import cross_origin
import typing as t
import json


###############################################################################
#                            Set Up Flask Blueprint                           #
###############################################################################
algorithm_status_blueprint = Blueprint("algorithm_status", __name__)

###############################################################################
#                Initiate algorithm status controller for route               #
###############################################################################
default_collection = 'apk'
algorithm_status_controller = AlgorithmStatusController(default_collection)


if t.TYPE_CHECKING:  # pragma: no cover
    from werkzeug.wrappers import Response as BaseResponse
    from .wrappers import Response
    import typing_extensions as te


@algorithm_status_blueprint.route("/status/get/<uuid>/<algorithm>", methods=['GET'])
@cross_origin()
def get(uuid: str, algorithm: str) -> t.Tuple[str, int]:
    """
    Method for getting status of one algorithm
    """
    if request.method == "GET":

        res = algorithm_status_controller.get(uuid, algorithm)

        return json.dumps(res), 200
    else:
        return f'{ request.method } not valid', 400


@algorithm_status_blueprint.route("/status/update/<uuid>/<algorithm>", methods=['GET', 'POST'])
@cross_origin()
def post(uuid: str, algorithm: str) -> t.Tuple[t.Dict, int]:
    """
    Method for posting/updating status of one algorithm
    """
    if request.method == "POST":

        new_status = request.json
        res = algorithm_status_controller.post(uuid, algorithm, **new_status)

        return res, 200
    else:
        return {"Error": f'{ request.method } not valid' }, 400


@algorithm_status_blueprint.route("/status/update/<uuid>/<algorithm>/<attribute>", methods=['GET', 'POST'])
@cross_origin()
def update_one_attr(uuid: str, algorithm: str, attribute: str) -> t.Tuple[str, int]:
    """
    Method for updating one attribute inside status of each and every algorithm
    """
    if request.method == "POST":
        # Assume new attribute value is a string
        update = str( request.data.decode() )

        res = algorithm_status_controller.update_status_attribute(uuid, algorithm, attribute, update)

        return safe_serialize( res ), 200
    else:
        return request.method + " not valid", 400

if __name__ == "__main__":
    pass
