from flask import Blueprint, request
from flask_cors import cross_origin

from controllers.algorithm_status_controller import AlgorithmStatusController
from controllers.job_status_controller import JobStatusController

status_blueprint = Blueprint('status', __name__, url_prefix='/status')

status_controller = JobStatusController('apk')
algorithm_status_controller = AlgorithmStatusController('apk')

@status_blueprint.route('/get/<uuid>', defaults={'algorithm': None}, methods=['GET'])
@status_blueprint.route('/get/<uuid>/<algorithm>', methods=['GET'])
@cross_origin()
def get_status(uuid, algorithm=None):
    """
    Get the status of a given uuid

    Path: /status/get/<uuid>
    Vars:
        uuid: The uuid of the status to get
        algorithm: The algorithm to get the status of
    """
    if request.method == "GET":
        if algorithm is None:
            return status_controller.get(uuid), 200
        else:
            return algorithm_status_controller.get(uuid, algorithm), 200
    return "Fail", 500


@status_blueprint.route('/update/<uuid>', defaults={'algorithm': None}, methods=['POST'])
@status_blueprint.route('/update/<uuid>/<algorithm>', methods=['POST'])
@cross_origin()
def update_status(uuid, algorithm=None):
    """
    Add a result to the database

    Path: /status/update/<uuid>/<algorithm>
    Vars:
        uuid: The uuid of the result to add
        algorithm: The algorithm to add the result of
    Body:
        {
            "status": str
        }
    """

    new_status = request.json
    print("uuid: ", str(uuid))
    print("algorithm: ", str(algorithm))

    if request.method == "POST":
        if algorithm is None:
            return status_controller.post(uuid, **new_status), 200
        else:
            return algorithm_status_controller.post(uuid, algorithm, **new_status), 200
    return "Fail", 500
