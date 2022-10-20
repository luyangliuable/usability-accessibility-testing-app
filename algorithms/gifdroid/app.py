import typing as t
import flask
from flask import request
import json
import os
from execute import _service_execute_gifdroid


app = flask.Flask(__name__)
###############################################################################
#        Load user config file gifdroid algorithm running configuration       #
###############################################################################

with open("config.json", "r") as f:
    config = json.load(f)

status_api = os.environ.get("STATUS_API")
file_api = os.environ.get("FILE_API")
flask_backend = os.environ.get( "FLASK_BACKEND" )


@app.route("/new_job", methods=["POST"])
def send_uid_and_signal_run() -> t.Tuple[t.Dict, int]:
    """
    This function creates a new job for gifdroid and droidbot to run together.

    POST req input:
    uid - The unique ID for tracking all the current task.
    """

    if request.method == "POST":
        droidbot_result_folder = request.get_json()["utg_path"]
        output_dir = request.get_json()["output_dir"]
        gif_path = request.get_json()["gif_path"]

        print(droidbot_result_folder)

        # Execute gifdroid ############################################################
        _service_execute_gifdroid(droidbot_result_folder, gif_path, output_dir)

        return {"result": "SUCCESS"}, 200
    
    return {"result": "FAILED", "message": "No HTTP POST method received"}, 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3005)
