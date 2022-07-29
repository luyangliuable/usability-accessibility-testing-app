from flask import Blueprint, request, jsonify
from redis import Redis
# from celery.result import AsyncResult
from flask_cors import cross_origin
# from werkzeug.datastructures import FileStorage
# from werkzeug.utils import secure_filename
from tasks import create_task, celery
import boto3
import json
import shutil
import tempfile
import json
import uuid
import os
# import warnings
# import linecache
# import codecs
# import pickle
# import zlib

###############################################################################
#                            Set Up Flask Blueprint                           #
###############################################################################
upload_blueprint = Blueprint("upload", __name__)

###############################################################################
#                                  Set Up AWS                                 #
###############################################################################
AWS_PROFILE = 'localstack'
AWS_REGION = 'us-west-2'
ENDPOINT_URL = os.environ.get('S3_URL')
bucketname = "uploadbucket"

boto3.setup_default_session(profile_name=AWS_PROFILE)
s3_client = boto3.client("s3", region_name=AWS_REGION, endpoint_url=ENDPOINT_URL)

def unique_id_generator():
    res = "apk_file_" + str( uuid.uuid4() ) + ".apk"
    return res


@upload_blueprint.route('/upload/apk', methods=["GET", "POST"])
@cross_origin()
def upload():
    """
    This blueprint method acts as an api file uploader. It must be uploaded using form-data.
    The key in json for the apk file must be apk_file.
    """
    print("upload start...")
    # print(request.get_data())

    if request.method == "POST":
        ###############################################################################
        #                        If post http request received                        #
        ###############################################################################

        print("[0] Getting request from front-end")
        file = str( request.get_data() )

        ###############################################################################
        #                              Generate unique id                             #
        ###############################################################################

        file_key = "apk_file_" + unique_id_generator()

        ###############################################################################
        #                   Compress and byte serialise the apk file                  #
        ###############################################################################
        print("[1] Generating file")
        # r.set(file_key, pickle.dumps( file ))
        temp_dir = tempfile.gettempdir();
        filename = unique_id_generator()
        print(os.path.join(temp_dir, filename), "created")

        with open(os.path.join(temp_dir, filename), "w") as savefile:
            savefile.write(file)

        print("[2] Uploading to bucket")
        s3_client.upload_file(os.path.join(temp_dir, filename), bucketname, filename)

        print("[3] creating celery task")
        task = create_task.delay()

        print("[4] return celery task id and file key")
        return json.dumps({"file_key": str( file_key ), "task_id": task.id}), 200

    return json.dumps({"message": "failed to upload"}), 400


@upload_blueprint.route('/upload/health')
def _check_health():
    return "Upload Is Online"


@upload_blueprint.route("/upload/<task_id>", methods=["GET"])
def get_status(task_id):
    print('getting task id', task_id)

    task_result = celery.AsyncResult(task_id)

    print("task_result",task_result)

    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }

    return jsonify(result), 200


@upload_blueprint.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    header['Access-Control-Allow-Methods'] = '*'
    # response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,timeout')
    # Other headers can be added here if needed
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # response.headers.add('access-control-allow-headers', 'Content-Type')
    # response.headers.add('access-control-allow-headers', 'authorization')
    # response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response



if __name__ == "__main__":
    print(unique_id_generator())
    print(unique_id_generator())
    print(unique_id_generator())
    print(unique_id_generator())
