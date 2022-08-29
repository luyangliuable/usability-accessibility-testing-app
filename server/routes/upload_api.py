from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from tasks import run_algorithm, celery
import boto3
import json
import tempfile
import json
import uuid
import os
from redis import Redis
from models.DBManager import DBManager

###############################################################################
#                            Set Up Flask Blueprint                           #
###############################################################################
upload_blueprint = Blueprint("upload", __name__)

###############################################################################
#                            Start mongodb instance                           #
###############################################################################
mongo = DBManager.instance()

###############################################################################
#                                  Set Up AWS                                 #
###############################################################################
AWS_PROFILE = 'localstack'
AWS_REGION = 'us-west-2'
ENDPOINT_URL = os.environ.get('S3_URL')
BUCKETNAME = "apk-bucket"


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


        print("[0] Getting request from front-end")

        # To get files use request.files.get() ########################################
        # To get form data use request.form.get() #####################################

        ###############################################################################
        #                              Generate unique id                             #
        ###############################################################################

        # Unique id is used to identify a file for a cluster ###################
        unique_id = unique_id_generator()

        # Document template to be inserted into mongodb
        data = DBManager.get_format(unique_id)

        # File name is the original uploaded file name ################################
        file_key = request.form.get('filename')

        # File name is the original uploaded file name ################################

        print("[1] Uploading additional files")

        temp_dir = tempfile.gettempdir()

        for key, item in request.files.items():
        ###############################################################################
        #                          Save every additional file                         #
        ###############################################################################
            if key != "apk_file":
                print("additional files", item.name, "detected")

                temp_file_name = os.path.join(temp_dir, str( item.name ))

                with open(temp_file_name, "wb") as savefile:
                    savefile.write(item.read())
                    savefile.close()

                s3_client.upload_file(temp_file_name, BUCKETNAME, os.path.join( unique_id, str(item.filename) ))
                data = DBManager.get_format(unique_id)
                data["additional_files"].append({"algorithm": item.name, "type": item.content_type, "name": item.filename, "notes": ""})

        ###############################################################################
        #                Create a temporary file to store file content                #
        ###############################################################################
        print("[2] Generating apk file")

        temp_file_name = os.path.join(temp_dir, unique_id)

        with open(temp_file_name, "wb") as savefile:
            savefile.write(request.files.get('apk_file').read())
            savefile.close()

        ###############################################################################
        #                   Upload the temporary file to git bucket                   #
        ###############################################################################
        print("[3] Uploading apk to bucket")
        s3_client.upload_file(temp_file_name, BUCKETNAME, os.path.join( unique_id, file_key ))

        print("[4] Adding apk file meta data to mongo db")

        apk_file_note = "user uploaded apk file"

        data["apk"].append({"type": "apk", "name": file_key, "notes": apk_file_note})

        mongo.insert_document(data, mongo.get_database()["apk"])

        print("[5] return celery task id and file key")
        return json.dumps({"file_key": str( file_key ), "uuid": unique_id}), 200

    return json.dumps({"message": "failed to upload"}), 400


@upload_blueprint.route('/signal_start/<algorithm>', methods=["GET", "POST"])
@cross_origin()
def signal_start(algorithm):
    if request.method == "POST":
        print("[1] creating celery task")
        uuid = request.form.get("uuid")

        print("uuid is", uuid)
        print("start task for algorithm", algorithm)

###############################################################################
#                       Add algorithm status to mongodb                       #
###############################################################################

        task_info = {"uuid": uuid, "algorithm": algorithm}
        task = run_algorithm.delay(task_info)

        return json.dumps({"task_id": task.id, "task_for_algorithm": "algorithm"}), 200

    return json.dumps({"message": "No POST request received."}), 400



@upload_blueprint.route('/upload/health')
def check_health():
    return "Upload Is Online"


@upload_blueprint.route("/task/<task_id>", methods=["GET"])
def get_status(task_id):
    print('getting task id', task_id)

    task_result = celery.AsyncResult(task_id)

    print("task_result",task_result)

    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }

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


if __name__ == "__main__":
    print((unique_id_generator()))
