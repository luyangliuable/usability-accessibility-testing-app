from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from tasks import run_algorithm, celery
import boto3
import json
import tempfile
import json
import uuid
import sys, os
from redis import Redis
from models.DBManager import DBManager
from controllers.algorithm_status_controller import AlgorithmStatusController
from controllers.upload_controller import UploadController

###############################################################################
#                            Set Up Flask Blueprint                           #
###############################################################################
upload_blueprint = Blueprint("upload", __name__)

###############################################################################
#                            Start mongodb instance                           #
###############################################################################
mongo = DBManager.instance()
collection_name = 'apk'

###############################################################################
#                                  Set Up AWS                                 #
###############################################################################
AWS_PROFILE = 'localstack'
AWS_REGION = 'us-west-2'
ENDPOINT_URL = os.environ.get('S3_URL')
BUCKETNAME = "apk-bucket"

uc = UploadController('apk')


boto3.setup_default_session(profile_name=AWS_PROFILE)
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    endpoint_url=ENDPOINT_URL
)


def unique_id_generator():
    res = str( uuid.uuid4() )
    return res


@upload_blueprint.route('/upload', methods=["GET", "POST"])
@cross_origin()
def upload():
    """
    This blueprint method acts as an api file uploader. It must be uploaded using form-data.
    The key in json for the apk file must be apk_file.
    """
    if request.method == "POST":
        ###############################################################################
        #                        If post http request received                        #
        ###############################################################################
        enforce_bucket_existance([BUCKETNAME, "storydistiller-bucket", "xbot-bucket"])

        data = uc.upload(request.files)

        ret = {'uuid': data['uuid'], 'apk': data['apk']['name']}
        return json.dumps(ret), 400

    return json.dumps({"message": "failed to upload"}), 400


@upload_blueprint.route('/signal_start/<uuid>', methods=["GET", "POST"])
@cross_origin(uuid)
def signal_start(uuid):
    if request.method == "POST":
        if request.json != None:
            print("uuid is", uuid)

            algorithms_to_complete_key = "algorithmsToComplete"

            algorithms_to_complete = request.json[algorithms_to_complete_key]

            print("algorithm to complete is", algorithms_to_complete)

            print("start task for algorithm", algorithms_to_complete[0]['uuid'])

            ###############################################################################
            #                       Add algorithm status to mongodb                       #
            ###############################################################################
            task_info = {"uuid": uuid, "algorithm": algorithms_to_complete[0]['uuid']}

            task = run_algorithm.delay(task_info)

            return json.dumps({"task_id": task.id, "task_for_algorithm": "algorithm"}), 200
        else:
            return "No request body for starting algorithms", 400

    return json.dumps({"message": "No POST request received."}), 400


@upload_blueprint.route('/upload/health')
def check_health() -> str:
    return "Upload Is Online"


@upload_blueprint.route("/task/<task_id>", methods=["GET"])
def get_status(task_id):

    stopPrint()
    task_result = celery.AsyncResult(task_id)

    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    allowPrint()

    return json.dumps(result), 200


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


def enforce_bucket_existance(buckets):
    for bucket in buckets:
        try:
            s3_client.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
        except:
            print("Bucket already exists %s".format( bucket ))

def stopPrint():
    sys.stdout = open(os.devnull, 'w')

def allowPrint():
    sys.stdout = sys.__stdout__


if __name__ == "__main__":
    print((unique_id_generator()))
