from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from tasks import create_task, celery
import datetime
import boto3
import json
import tempfile
import json
import uuid
import os
from redis import Redis
from models.Apk import ApkManager
# from celery.result import AsyncResult
# from werkzeug.datastructures import FileStorage
# from werkzeug.utils import secure_filename
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
#                            Set Up Flask Blueprint                           #
###############################################################################

mongo = ApkManager.instance()
# mongo.create_mongo.insert_document({"filename": "test.apk"}, mongo.get_database()["apk"])

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
    res = str( uuid.uuid4() )
    return res


@upload_blueprint.route('/upload/apk', methods=["GET", "POST"])
@cross_origin()
def upload():
    """
    This blueprint method acts as an api file uploader. It must be uploaded using form-data.
    The key in json for the apk file must be apk_file.
    """
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

        unique_id = unique_id_generator()
        file_key = unique_id + ".apk"

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
        s3_client.upload_file(os.path.join(temp_dir, filename), bucketname, "/" + unique_id + "/" + file_key)

        print("[3] Adding file data to mongodb")
        mongo.insert_document({"type": "apk", "uuid": unique_id, "date": str( datetime.datetime.now() )}, mongo.get_database()["apk"])

        print("[4] creating celery task")
        task = create_task.delay()

        print("[5] return celery task id and file key")
        return json.dumps({"file_key": str( file_key ), "task_id": task.id}), 200

    return json.dumps({"message": "failed to upload"}), 400


@upload_blueprint.route('/upload/health')
def check_health():
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
