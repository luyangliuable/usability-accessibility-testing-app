import pymongo
import boto3
import json
import os
from os import path
import subprocess
import tempfile
from flask import Flask, request, jsonify

app = Flask(__name__)

###############################################################################
#        Load user config file gifdroid algorithm running configuration       #
###############################################################################

with open("config.json", "r") as f:
    config = json.load(f)

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

            # Execute gifdroid ############################################################
            _service_execute_gifdroid(uid)
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
    print("[4] Saving utg.js file to bucket.")

    enforce_bucket_existance([config[ "BUCKETNAME" ], "storydistiller-bucket", "xbot-bucket"])

    s3_client.upload_file(config[ "DEFAULT_UTG_FILENAME" ], config[ 'BUCKETNAME' ], os.path.join(uuid, config[ "DEFAULT_UTG_FILENAME" ]))

    ###############################################################################
    #                                Update mongodb                               #
    ###############################################################################

    print("[5] Updating database for traceability of utg file")
    print("Saving into entry", uuid)

    _db.apk.update_one(
        {
            "uuid": uuid
        },
        {
            "$set": {
                "utg_files": config["DEFAULT_UTG_FILENAME"]
            }
        }
    )

    os.chdir("/home/droidbot/")



def _service_execute_gifdroid(uuid):
    # retrieve utg file name from mongodb

    print("[1] Getting utg filename from mongodb")

    cursor = _db['apk'].find({})

    for document in cursor:
        # Find document that match with current uuid.
        if document["uuid"] == uuid:
            print(str( document ))
            utg_filename = document['utg_files']

    print(utg_filename)

    print("[2] Creating temporary file to save utg file")
    temp_dir = tempfile.gettempdir()

    target_utg = path.join(temp_dir, utg_filename)

    s3_client.download_file(
        Bucket=config["BUCKETNAME"],
        Key=path.join(uuid, utg_filename),
        Filename = target_utg
    )

    #run gifdroid

    print("[3] Running GIFDROID app")

    subprocess.run([ "adb", "connect", config['EMULATOR']])

    os.chdir("/home/gifdroid")
    subprocess.run([ "python3", "main.py", "--video=../sample.gif", "--utg=" + target_utg, "--artifact=artifact", "--out=" + config["OUTPUT_FILE"]])

    #save output file to bucket
    enforce_bucket_existance([config[ "BUCKETNAME" ], "storydistiller-bucket", "xbot-bucket"])


    print("[4] Uploading gif file to bucket")
    s3_client.upload_file(config[ "DEFAULT_GIF_FILENAME" ], config[ 'BUCKETNAME' ], config[ "DEFAULT_GIF_FILENAME" ])

    #update mongodb
    print("[5] Updating mongodb for traceability")
    _db.apk.update_one(
        {
            "uuid": uuid
        },
        {
            "$set": {
                "gifdroid_files": [config["DEFAULT_GIF_FILENAME"]]
            }
        }
    )


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
