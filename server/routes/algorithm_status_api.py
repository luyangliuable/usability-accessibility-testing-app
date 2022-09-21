from flask import Blueprint, request
from flask_cors import cross_origin
import json
import uuid
from controllers.algorithm_status_controller import *
import typing as t


###############################################################################
#                            Set Up Flask Blueprint                           #
###############################################################################
algorithm_status_blueprint = Blueprint("algorithm_status", __name__)

###############################################################################
#                Initiate algorithm status controller for route               #
###############################################################################
default_collection = 'apk'
asc = AlgorithmStatusController(default_collection)


if t.TYPE_CHECKING:  # pragma: no cover
    from werkzeug.wrappers import Response as BaseResponse
    from .wrappers import Response
    import typing_extensions as te


@algorithm_status_blueprint.route("/status/update/<uuid>/<algorithm>", methods=['GET', 'POST'])
@cross_origin()
def update_algorthm_status(uuid: str, algorithm: str) -> t.Tuple[str, int]:
    """
    Method for updating status of each and every algorithm
    """
    if request.method == "POST":
        status = str( request.data.decode() )

        res = asc.update(uuid, algorithm, status=status)

        res = ""
        return res, 200

    return "Invalid request", 400


@algorithm_status_blueprint.route("/status/get/<uuid>/<algorithm>", methods=['GET'])
@cross_origin()
def get(uuid: str, algorithm: str) -> t.Tuple[str, int]:
    """
    Method for updating status of each and every algorithm
    """
    if request.method == "GET":

        res = asc.get(uuid, algorithm)

        return json.dumps(res), 200
    else:
        return request.method + " not valid", 400


@algorithm_status_blueprint.route("/status/update/<uuid>/<algorithm>", methods=['GET', 'POST'])
@cross_origin()
def update(uuid: str, algorithm: str) -> t.Tuple[str, int]:
    """
    Method for updating status of each and every algorithm
    """
    if request.method == "POST":

        status = str( request.data.decode() )
        res = asc.update(uuid, algorithm, status)

        return json.dumps(res), 200
    else:
        return request.method + " not valid", 400


@algorithm_status_blueprint.route("/status/update/<uuid>/<algorithm>/<attribute>", methods=['GET', 'POST'])
@cross_origin()
def update_one_attr(uuid: str, algorithm: str, attribute: str) -> t.Tuple[str, int]:
    """
    Method for updating one attribute inside status of each and every algorithm
    """
    if request.method == "POST":
        # Assume new attribute value is a string
        update = str( request.data.decode() )

        res = asc.update_algorithm_status_attribute(uuid, algorithm, attribute, update)

        return safe_serialize( res ), 200
    else:
        return request.method + " not valid", 400

# @algorithm_status_blueprint.route("/status/test", methods=['GET'])
# @cross_origin()
# def p_status():
#     threading.Thread(target=test, args=(1,))

#     return "Started thread", 200


# @algorithm_status_blueprint.route("/status/test2", methods=['GET'])
# @cross_origin()
# def c_status():
#     print("started")
#     time.sleep(2000)
#     return "finished thread", 200

def test(name):
    logging.info("Thread %s: starting", name)
    time.sleep(200)
    logging.info("Thread %s: finishing", name)


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
