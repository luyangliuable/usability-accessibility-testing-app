from os.path import isfile
from flask import Blueprint, send_file
from flask_cors import cross_origin
import boto3
import typing as t
import os, shutil

from download_parsers.gifdroid_json_parser import gifdroidJsonParser
from controllers.download_controller import DownloadController

###############################################################################
#                            Set Up Flask Blueprint                           #
###############################################################################
download_blueprint = Blueprint("download", __name__)

if t.TYPE_CHECKING:  # pragma: no cover
    from werkzeug.wrappers import Response as BaseResponse
    from .wrappers import Response
    import typing_extensions as te


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

download_controller = DownloadController('apk', gifdroidJsonParser)

@download_blueprint.route('/download_result/<uuid>/<algorithm>/<type>/<name>', methods=["GET"])
@cross_origin()
def download(uuid, algorithm, name, type) -> t.Tuple["Response", int]:
    result_file_from_algorithm = download_controller.get(uuid, algorithm, type, name)

    return send_file(result_file_from_algorithm, as_attachment=True), 200


@download_blueprint.route('/download_result/zipped/<uuid>/', methods=["GET", "POST"])
@cross_origin()
def download_zipped(uuid: str) -> t.Tuple["Response", int]:
    ###############################################################################
    #                         Download file from s3 bucket                        #
    ###############################################################################
    result_summary_zip_from_job = download_controller.download_all_objects_in_folder(uuid)

    archive_type = 'zip'
    print("Getting summary files from", result_summary_zip_from_job)

    cwd = os.getcwd()

    if os.path.isdir(result_summary_zip_from_job):
        zipped_file = shutil.make_archive(uuid, archive_type, result_summary_zip_from_job, cwd)
    else:
        raise RuntimeError("Failed to get summary files to zip from", result_summary_zip_from_job)

    shutil.rmtree(result_summary_zip_from_job)

    result = os.path.join(cwd, zipped_file)

    return send_file(result, as_attachment=True), 200

