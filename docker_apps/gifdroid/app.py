import pymongo
import boto3
import os
from os import path
import subprocess
import tempfile
from flask import Flask, request, jsonify

app = Flask(__name__)

# aws info for development environment
AWS_REGION = 'us-west-2'
AWS_PROFILE = 'localstack'
ENDPOINT_URL = os.environ.get('S3_URL')

# aws s3 client
boto3.setup_default_session(profile_name=AWS_PROFILE)
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    endpoint_url=ENDPOINT_URL,
)

###############################################################################
#                              Connect to mongodb                             #
###############################################################################
try:
    connection = pymongo.MongoClient(os.environ.get('MONGO_URL'))
    _db = connection.fit3170
    connection.server_info()  # Triger exception if connection fails to the database
except Exception as ex:
    print('failed to connect', ex)
else:
    print("Successfully connected to mongodb.")

# route for starting new job
@app.route("/new_job", methods=["POST"])
def send_uid_and_signal_run():
    if request.method == "POST":
        try:
            print('NEW JOB FOR UUID: ' + request.get_json()["uid"])
            uid = request.get_json()["uid"]
            _service_execute_droidbot(uid)
        except Exception as ex:
            print(ex)
            return str( ex )

        return jsonify( {"result": "SUCCESS"} ), 200

    return "No HTTP POST method received"

# executing new job
def _service_execute_droidbot(uuid):
    print('Beginning new job for %s' % uuid)

    ###############################################################################
    #                      GET the APK file name from mongodb                     #
    ###############################################################################
    print("[1] Getting session information")
    cursor = _db['apk'].find({})

    for document in cursor:
        if document["uuid"] == uuid:
            apk_filename = document['apk'][0]['name']

    ############################################################################
    #                    Download file into temporary folder                   #
    ############################################################################
    temp_dir = tempfile.gettempdir()

    print("[2] Getting file from bucket using UUID " + uuid + " and apk file " + apk_filename + ".")
    print(temp_dir)

    target_apk = path.join(temp_dir, apk_filename)
    # s3_client.download_file('apk-bucket', path.join(uuid, apk_filename), target_apk)
    s3_client.download_file(
        Bucket='apk-bucket',
        Key=path.join(uuid, apk_filename),
        Filename = target_apk
    )

   ############################################################################
   #                       Run program with download apk                      #
   ############################################################################
    print("[3] Running Droidbot app")
    subprocess.run([ "adb", "connect", os.environ.get("EMULATOR")])
    os.chdir("/home/droidbot")
    subprocess.run([ "droidbot", "-a", target_apk, "-o", "./" ])


def _service_execute_gifdroid(uuid):
    # [0] TODO retrieve 

    # [1] TODO retrieve utg file from s3 bucket
    # uuid/utg.js

    # subprocess.run([ "python", "main.py", "--video=dsandsakndsal.gif" --utg=<utg.json> --artifact=<folder> --out=<out_filename> ])

    pass


@app.route("/", methods=["GET"])
def home():
    return "works."


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3005)
