from flask import Blueprint, request, jsonify, send_file
from flask_cors import cross_origin
import boto3
import json
import uuid
import os

from download_parsers.gifdroid_json_parser import gifdroidJsonParser
from controllers.download_controller import DownloadController

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

download_controller = DownloadController('apk', gifdroidJsonParser)

@download_blueprint.route('/download_result/<uuid>/<algorithm>/<name>', methods=["GET", "POST"])
@cross_origin()
def download(uuid, algorithm, name):
    result_file_from_algorithm = download_controller.download(uuid, algorithm, name)

    return send_file(result_file_from_algorithm, as_attachment=True), 200


@download_blueprint.route('/download_result/zipped/<uuid>/<algorithm>', methods=["GET", "POST"])
@cross_origin()
def download_zipped(uuid,algorithm):
    ###############################################################################
    #                         Download file from s3 bucket                        #
    ###############################################################################

    ###############################################################################
    #               TODO create download link to zipped output files              #
    ###############################################################################
    pass
