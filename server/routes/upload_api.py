from controllers.upload_controller import UploadController
from utility.enforce_bucket_existance import *
from models.DBManager import DBManager
from flask import Blueprint, request
from flask_cors import cross_origin
from tasks import worker
import sys, os
import json

###############################################################################
#                            Set Up Flask Blueprint                           #
###############################################################################
upload_blueprint = Blueprint("upload", __name__)
upload_controller = UploadController('apk')

###############################################################################
#                            Start mongodb instance                           #
###############################################################################
collection_name = 'apk'
mongo = DBManager.instance()


@upload_blueprint.route('/upload', methods=["GET", "POST"])
@cross_origin()
def post():
    """
    This blueprint method acts as an api file uploader. It must be uploaded using form-data.
    The key in json for the apk file must be apk_file.
    """
    if request.method == "POST":
        enforce_bucket_existance([ BUCKETNAME ])

        data = upload_controller.post(request.files)

        ret = {'uuid': data['uuid'], 'apk': data['apk']['name']}

        return json.dumps(ret), 200

    return json.dumps({"message": "failed to upload"}), 400


@upload_blueprint.route("/task/<task_id>", methods=["GET"])
def get(task_id):

    stopPrint()
    task_result = worker.AsyncResult(task_id)

    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    allowPrint()

    return json.dumps(result), 200


@upload_blueprint.route('/upload/health')
def _check_health() -> str:
    return "Upload Is Online"


@upload_blueprint.after_request
def after_request(response):
    """
        To allow cross origin requests because flask and react are not on the same url.
    """
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    header['Access-Control-Allow-Methods'] = '*'
    return response

def stopPrint():
    sys.stdout = open(os.devnull, 'w')

def allowPrint():
    sys.stdout = sys.__stdout__


if __name__ == "__main__":
    pass
