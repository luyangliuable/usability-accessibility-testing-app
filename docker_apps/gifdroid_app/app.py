from botocore import endpoint
from botocore.compat import accepts_kwargs
import pymongo
import boto3
import json
import requests
import os
from os import path
import subprocess
import tempfile
from flask import Flask, request, jsonify

from converter.run import convert_droidbot_to_gifdroid_utg

app = Flask(__name__)

###############################################################################
#        Load user config file gifdroid algorithm running configuration       #
###############################################################################

with open("config.json", "r") as f:
    config = json.load(f)

endpoint_url = os.environ.get("S3_URL")

if endpoint_url == None:
    endpoint_url = config['ENDPOINT_URL']

file_api = str( os.environ.get("FILE_API") )

if file_api == None:
    endpoint_url = config['FILE_API']

EMULATOR = os.environ.get( "EMULATOR" )

if EMULATOR == None:
    EMULATOR = config['EMULATOR']


###############################################################################
#                                Set up AWS S3                                #
###############################################################################


boto3.setup_default_session(profile_name=config[ 'AWS_PROFILE' ])
s3_client = boto3.client(
    "s3",
    region_name=config['AWS_REGION'],
    endpoint_url=endpoint_url,
)


###############################################################################
#                              Connect to mongodb                             #
###############################################################################
# try:
#     connection = pymongo.MongoClient(config["MONGODB"])
#     _db = connection.fit3170
#     connection.server_info()  # Triger exception if connection fails to the database
# except Exception as ex:
#     print('failed to connect', ex)
# else:
#     print("Successfully connected to mongodb.")


@app.route("/new_job", methods=["POST"])
def send_uid_and_signal_run():
    """
    This function creates a new job for gifdroid and droidbot to run together.

    POST req input:
    uid - The unique ID for tracking all the current task.
    """
    if request.method == "POST":
        print('NEW JOB FOR UUID: ' + request.get_json()["uid"])

        # Get the UUID from the request in json #######################################
        uid = request.get_json()["uid"]

        # Execute droidbot ############################################################
        _service_execute_droidbot(uid)

        # Execute gifdroid ############################################################
        _service_execute_gifdroid(uid)

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
    # cursor = _db['apk'].find({})

    # for document in cursor:
    #     # Find document that match with current uuid.
    #     if document["uuid"] == uuid:
    #         apk_filename = document['apk'][0]['name']

    response = requests.get(file_api, headers={'Content-Type': 'application/json'},  data=json.dumps( {'uuid': uuid} )).content

    ###############################################################################
    #          Fix flask backend return json not stupid byte string please         #
    ###############################################################################
    data = bytes_to_json(response)
    data = data[0]

    print("data")
    print(data)

    # Apk has an Array/List of apk files ##########################################
    apk_filename = data['apk'][0]['name']

    ############################################################################
    #                    Download file into temporary folder                   #
    ############################################################################
    temp_dir = tempfile.gettempdir()

    print("[2] Getting file from bucket using UUID " + uuid + " and apk file " + apk_filename + ".")
    print(temp_dir)

    target_apk = path.join(temp_dir, apk_filename)

    print(config['ENDPOINT_URL'])

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

    subprocess.run([ "adb", "connect", EMULATOR])

    os.chdir("/home/droidbot")
    subprocess.run([ "droidbot", "-count", config[ "NUM_OF_EVENT" ], "-a", target_apk, "-o", OUTPUT_DIR])

    ###############################################################################
    #                                Save utg file                                #
    ###############################################################################
    print("[4] Saving utg.js file to bucket.")

    enforce_bucket_existance([config[ "BUCKET_NAME" ], "storydistiller-bucket", "xbot-bucket"])

    #Upload events folder
    upload_directory("events", config["BUCKET_NAME"])

    #Upload states folder
    upload_directory("states", config["BUCKET_NAME"])

    # Upload utg
    s3_client.upload_file(config[ "DEFAULT_UTG_FILENAME" ], config[ 'BUCKET_NAME' ], os.path.join(uuid, config[ "DEFAULT_UTG_FILENAME" ]))

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

    ###############################################################################
    #                        Get utg filename from mongodb                        #
    ###############################################################################
    print("[1] Getting utg filename from mongodb")

    data = requests.post(file_api, headers={'Content-Type': 'application/json'}, data={'uuid': uuid}).json()[0]
    data = bytes_to_json(data)[0]

    utg_filename=data['utg_files']

    # cursor = _db['apk'].find({})

    # utg_filename=""

    # for document in cursor:
    #     # Find document that match with current uuid.
    #     if document["uuid"] == uuid:
    #         print(str( document ))
    #         utg_filename = document['utg_files']

    print(utg_filename)

    print("[2] Creating temporary file to save utg file")
    temp_dir = tempfile.gettempdir()

    target_utg = path.join(temp_dir, utg_filename)

    s3_client.download_file(
        Bucket=config["BUCKET_NAME"],
        Key=path.join(uuid, utg_filename),
        Filename = target_utg
    )

    ###############################################################################
    #                        Convert utg to correct format                        #
    ###############################################################################
    convert_droidbot_to_gifdroid_utg(os.path.join("/home/droidbot", config['DEFAULT_UTG_FILENAME']),"/home/droidbot/events", "home/droidbot/states")

    ###############################################################################
    #                          Get gif file from frontend                         #
    ###############################################################################

    ###############################################################################
    #                               Run GIFDROID app                              #
    ###############################################################################
    print("[3] Running GIFDROID app")

    subprocess.run([ "adb", "connect", EMULATOR])

    os.chdir("/home/gifdroid")
    subprocess.run([ "python3", "main.py", "--video=../sample.gif", "--utg=" + "./utg.json", "--artifact=./output", "--out=" + config["OUTPUT_FILE"]])

    #save output file to bucket
    enforce_bucket_existance([config[ "BUCKET_NAME" ], "storydistiller-bucket", "xbot-bucket"])


    print("[4] Uploading gif file to bucket")
    s3_client.upload_file(config[ "DEFAULT_GIF_FILENAME" ], config[ 'BUCKET_NAME' ], config[ "DEFAULT_GIF_FILENAME" ])

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

###############################################################################
#                              Utility Functions                              #
###############################################################################

def bytes_to_json(byte_str: bytes):
    data = byte_str.decode('utf8').replace("'", '"')
    data = json.loads(data)

    return data

def upload_directory(path, bucketname):
    for root,dirs,files in os.walk(path):
        for file in files:
            s3_client.upload_file(os.path.join(root,file),bucketname,file)


def enforce_bucket_existance(buckets):
    for bucket in buckets:
        try:
            s3_client.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
        except:
            print("Bucket already exists %s".format( bucket ))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3005)
