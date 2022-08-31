import boto3
import json
import uuid
import os
from controllers.update_document_controller import UpdateDocumentController as UDContrl
from utility.uuid_generator import unique_id_generator
from download_parsers.strategy import Strategy

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

class DownloadController:
    def __init__(self, collection_name: str, json_result_file_parser: Strategy):
        self.cn = collection_name
        self.udc = UDContrl(collection_name, json_result_file_parser)

    def download(self,uuid, algorithm, name):

        s3_client.download_file(Bucket='apk-bucket', Key=os.path.join(uuid, name), Filename=name)

        return name
