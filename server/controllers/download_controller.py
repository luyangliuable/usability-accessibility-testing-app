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


    def download(self, uuid, algorithm, type, name):
        # if algorithm == "gifdroid":
        #     algorithm = "gifdroid"

        # print(algorithm)
        # print(os.path.join(uuid, algorithm ,name))

        path = ""
        output = ""

        if algorithm == "gifdroid":
            output = "gifdroid.json"
            path = os.path.join(uuid, algorithm , output)
        elif algorithm == "xbot":
            # For issues type is issues
            if type == "issues":
                output = name+".txt"
                path = os.path.join(uuid, "activity", name, algorithm, type, output)
            if type == "images":
                output = name+".png"
                path = os.path.join(uuid, "activity", name, algorithm, type, output)
        elif algorithm == "owleye":
            output = name+".jpg"
            path = os.path.join(uuid, "activity", name, algorithm, output)
        elif algorithm == "activity":
            if type == "images":
                output = name+".jpg"
                path = os.path.join(uuid, "activity", name, type, name+".png")

        print("Downloading from", path)
        print("Filename is", output)

        s3_client.download_file(Bucket='apk-bucket', Key=path, Filename=output)

        return output
