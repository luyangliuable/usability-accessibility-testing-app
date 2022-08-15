import pymongo
import boto3
import os
from os import path
import subprocess
import tempfile
from flask import Flask, request, jsonify

app = Flask(__name__)

config = {
    'AWS_REGION': 'us-west-2',
    "AWS_PROFILE": 'localstack',
    "ENDPOINT_URL": os.environ.get('S3_URL'),
    "BUCKETNAME": "gifdroid-bucket",
    "MONGODB": os.environ.get('MONGO_URL'),
    "DEFAULT_UTG_FILENAME":  "utg.js",
    "NUM_OF_EVENT": "10",
    "EMULATOR": os.environ.get("EMULATOR"),
}

###############################################################################
#                                Set up AWS S3                                #
###############################################################################

boto3.setup_default_session(profile_name=config[ 'AWS_PROFILE' ])
s3_client = boto3.client(
    "s3",
    region_name=config['AWS_REGION'],
    endpoint_url=config['ENDPOINT_URL'],
)


###############################################################################
#                              Connect to mongodb                             #
###############################################################################
try:
    connection = pymongo.MongoClient(config["MONGODB"])
    _db = connection.fit3170
    connection.server_info()  # Triger exception if connection fails to the database
except Exception as ex:
    print('failed to connect', ex)
else:
    print("Successfully connected to mongodb.")


@app.route("/new_job", methods=["POST"])
def send_uid_and_signal_run():
    """
    This function creates a new job for gifdroid and droidbot to run together.

    POST req input:
    uid - The unique ID for tracking all the current task.
    """

    if request.method == "POST":
        try:
            print('NEW JOB FOR UUID: ' + request.get_json()["uid"])

            # Get the UUID from the request in json #######################################
            uid = request.get_json()["uid"]

            # Execute droidbot ############################################################
            _service_execute_droidbot(uid)

            # TODO execute gifdroid
        except Exception as ex:
            print(ex)

            return str( ex )

        return jsonify( {"result": "SUCCESS"} ), 200

    return "No HTTP POST method received"


def _service_execute_droidbot(uuid):
    """
    This function execute droidbot algorithm responsible for getting the utg.js file.

    Parameters:
        uuid - The unique id for the current task.
    """

    print('Beginning new job for %s' % uuid)

    ###############################################################################
    #                      GET the APK file name from mongodb                     #
    ###############################################################################
    print("[1] Getting session information")
    cursor = _db['apk'].find({})

    for document in cursor:
        # Find document that match with current uuid.

        if document["uuid"] == uuid:
            apk_filename = document['apk'][0]['name']

    ############################################################################
    #                    Download file into temporary folder                   #
    ############################################################################
    temp_dir = tempfile.gettempdir()

    print("[2] Getting file from bucket using UUID " + uuid + " and apk file " + apk_filename + ".")
    print(temp_dir)

    target_apk = path.join(temp_dir, apk_filename)

    s3_client.download_file(
        Bucket='apk-bucket',
        Key=path.join(uuid, apk_filename),
        Filename = target_apk
    )

    ############################################################################
    #                      Run program with downloaded apk                     #
    ############################################################################
    OUTPUT_DIR = "./"

    print("[3] Running Droidbot app")

    subprocess.run([ "adb", "connect", config['EMULATOR']])

    os.chdir("/home/droidbot")
    subprocess.run([ "droidbot", "-count", config[ "NUM_OF_EVENT" ], "-a", target_apk, "-o", OUTPUT_DIR])


    ###############################################################################
    #                                Save utg file                                #
    ###############################################################################
    print("[4] Saving uTG.js file to bucket.")

    enforce_bucket_existance([config[ "BUCKETNAME" ], "storydistiller-bucket", "xbot-bucket"])

    s3_client.upload_file(config[ "DEFAULT_UTG_FILENAME" ], config[ 'BUCKETNAME' ], config[ "DEFAULT_UTG_FILENAME" ])

    ###############################################################################
    #                                Update mongodb                               #
    ###############################################################################
    print("[5] Updating database for traceability of utg file")

    _db.apk.update_one(
        {
            "uuid": uuid
        },
        {
            "$set": {
                "utg_files": DEFAULT_UTG_FILENAME
            }
        }
    )


def _service_execute_gifdroid(uuid):
    # [0] TODO retrieve

    # [1] TODO retrieve utg file from s3 bucket
    # uuid/utg.js

    # subprocess.run([ "python", "main.py", "--video=dsandsakndsal.gif" --utg=<utg.json> --artifact=<folder> --out=<out_filename> ])

    pass


@app.route("/", methods=["GET"])
def check_health():
    """
    Check that gifdroid is in good health.
    """

    return "Gifdroid is live!"


def enforce_bucket_existance(buckets):
    for bucket in buckets:
        try:
            s3_client.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
        except:
            print("Bucket already exists %s".format( bucket ))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3005)
