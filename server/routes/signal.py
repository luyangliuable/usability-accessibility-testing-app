from flask import Blueprint, request
from flask_cors import cross_origin
from controllers.algorithm_task_controller import *

# Initialise the blueprint
# Specifies the prefix for all routes in this file
signals_blueprint = Blueprint('signal', __name__, url_prefix='/signal')

# Initialise the controller
algorithm_task_controller = AlgorithmTaskController('apk')


@signals_blueprint.route('/start/<uuid>', methods=['POST'])
@cross_origin()
def start(uuid):
    """
    Signal to start the processing of a given uuid

    Path: /signal/start/<uuid>
    Vars:
        uuid: The uuid of the process to start
    """

    if request.method == "POST":
        if request.json != None:
            algorithms = request.json["algorithmsToComplete"]
            algorithms_to_complete = [AlgorithmEnum[algorithm['uuid']].value for algorithm in algorithms]
            print("algorithms_to_complete: ", str(algorithms_to_complete))

            algorithm_task_controller.post(uuid, algorithms_to_complete)

            return json.dumps({"uuid": uuid, "algorithms": algorithms_to_complete}), 200
        else:
            return "Fail: No request body", 400

    return json.dumps({"message": "No POST request received."}), 400


@signals_blueprint.route('/stop/<uuid>', methods=['POST'])
@cross_origin()
def stop(uuid):
    """

    Signal to stop the processing of a given uuid

    Path: /signal/stop/<uuid>
    Vars:
        uuid: The uuid of the result to get


    TODO: Implement this method

    """

    return "get_result", 200


@signals_blueprint.route('/delete/<uuid>', methods=['POST'])
@cross_origin()
def delete(uuid):
    """

    Not sure about this one?

    Path: /signal/delete/<uuid>
    Vars:
        uuid: The uuid of the result to add
    Body:
        {
            "files": [str],
            "type": str,
            "names": [str]
        }

    TODO: Implement this method
    """

    return "add_result", 200
