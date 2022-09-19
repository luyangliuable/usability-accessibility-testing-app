from flask import Blueprint, request
from flask_cors import cross_origin
from controllers.job_status_controller import *
import typing as t
import json


###############################################################################
#                            Set Up Flask Blueprint                           #
###############################################################################
job_status_blueprint = Blueprint("job_status", __name__)

###############################################################################
#                Initiate algorithm status controller for route               #
###############################################################################
DEFAULT_COLLECTION = 'apk'
jsc = JobStatusController(DEFAULT_COLLECTION)


if t.TYPE_CHECKING:  # pragma: no cover
    from werkzeug.wrappers import Response as BaseResponse
    from .wrappers import Response
    import typing_extensions as te


@job_status_blueprint.route("/status/get/<uuid>", methods=['GET'])
@cross_origin()
def get(uuid: str) -> t.Tuple[str, int]:
    """
    Method for getting a status of each and every algorithm
    """
    if request.method == "GET":
        res = jsc.get(uuid)

        return res, 200

    return "Invalid request", 400


@job_status_blueprint.route("/status/update/<uuid>", methods=['GET', 'POST'])
@cross_origin()
def update(uuid: str) -> t.Tuple[t.Dict, int]:
    """
    Method for updating status of each and every algorithm
    """
    if request.method == "POST":
        status = str( request.data.decode() )

        res = jsc.update(uuid, status)

        return res, 200
    else:
        return {"error": request.method + " not valid" }, 400
