from flask import Blueprint, request, jsonify, send_file
from flask_cors import cross_origin
import requests
import boto3
import json
import tempfile
import json
import uuid
import os
from redis import Redis
from models.Apk import ApkManager

###############################################################################
#                            Set Up Flask Blueprint                           #
###############################################################################
download_blueprint = Blueprint("download", __name__)

###############################################################################
#                                  Set Up AWS                                 #
###############################################################################
AWS_PROFILE = 'localstack'
AWS_REGION = 'us-west-2'
ENDPOINT_URL = os.environ.get('S3_URL')
print(ENDPOINT_URL)
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


@download_blueprint.route('/download_result/<uuid>/<algorithm>', methods=["GET", "POST"])
@cross_origin()
def download(uuid,algorithm):
    ###############################################################################
    #                         Download file from s3 bucket                        #
    ###############################################################################

    data = {'uuid': uuid}

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    response = requests.get('http://localhost:5000/file/get', data=json.dumps( data ), headers=headers)

    ###############################################################################
    #             Assume the the first element in result is the result            #
    ###############################################################################
    lookup = json.loads( response.content )[0]

    ###############################################################################
    #      If the file is json just respond with json instead of sendinf file     #
    ###############################################################################

    ###############################################################################
    #                    Assume first element of apk is the apk                   #
    ###############################################################################
    result_file_from_algorithm = lookup[algorithm][0]['name']

    ###############################################################################
    #                        TODO Update more buckets here                        #
    ###############################################################################
    result_bucket = None
    if algorithm == 'apk':
        result_bucket = 'apk-bucket'
    elif algorithm == "gifdroid_file":
        result_bucket = 'gifdroid-bucket'
    else:
        return "Invalid Algorithm", 400

    print("Getting file from", os.path.join(uuid, result_file_from_algorithm))

    s3_client.download_file(Bucket=result_bucket, Key=os.path.join(uuid, result_file_from_algorithm), Filename=result_file_from_algorithm)

    return send_file(result_file_from_algorithm, as_attachment=True), 200
