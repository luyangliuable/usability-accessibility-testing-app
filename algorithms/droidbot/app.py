from execute import _service_execute_droidbot
import typing as t
import flask
from flask import request
import json
import os
from time import sleep


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

    if request.method != "POST":
        return {"result": "FAILED", "message": "No HTTP POST method received"}, 400
    
    apk_path = request.get_json()["apk_path"]
    output_dir = request.get_json()["output_dir"]
    # uuid = request.get_json()["uuid"]
    
    # Execute droidbot ############################################################
    print(f"Droidbot container: Recieved request for {apk_path}. output_dir: {output_dir}")
    for attempt in range(3):
        _service_execute_droidbot(apk_path=apk_path, output_dir=output_dir)
        
        # attempt to run droidbot 3 times
        if os.path.exists(os.path.join(output_dir, 'states')) and \
            len(os.listdir(os.path.join(output_dir, 'states'))) > 0:
            return {"result": "SUCCESS"}, 200
        
        print("Attempt to run Droidbot failed, trying again")
        sleep(2)
    
    return {"result": "FAILED"}, 500

    

    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3008)
