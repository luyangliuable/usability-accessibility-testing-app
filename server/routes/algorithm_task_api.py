from controllers.algorithm_task_controller import *
from utility.enforce_bucket_existance import *
from flask import Blueprint, request
from flask_cors import cross_origin
import json

###############################################################################
#                            Set Up Flask Blueprint                           #
###############################################################################
blueprint_name = "algorithm_task"
algorithm_task_blueprint = Blueprint(blueprint_name, __name__)
algorithm_task_controller = AlgorithmTaskController('apk')


@algorithm_task_blueprint.route('/signal_start/<uuid>', methods=["GET", "POST"])
@cross_origin()
def start_job(uuid):
    if request.method == "POST":
        if request.json != None:
            algorithms_to_complete_key = "algorithmsToComplete"
            algorithms_to_complete = request.json[algorithms_to_complete_key]

            algorithm_task_controller.post(uuid, algorithms_to_complete)

            return json.dumps({"uuid": uuid, "algorithms": algorithms_to_complete}), 200
        else:
            return f'No request body for {blueprint_name}', 400

    return json.dumps({"message": "No POST request received."}), 400


@algorithm_task_blueprint.route('/signal_start')
def check_health() -> str:
    return f'{blueprint_name} Is Online'


@algorithm_task_blueprint.after_request
def after_request(response):
    """
        To allow cross origin requests because flask and react are not on the same url.
    """
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    header['Access-Control-Allow-Methods'] = '*'
    return response

if __name__ == "__main__":
    pass
