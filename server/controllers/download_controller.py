import boto3
import os
from controllers.update_document_controller import UpdateDocumentController as UDContrl
from download_parsers.strategy import Strategy
from typing import TypeVar, Generic

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

T = TypeVar('T')

class DownloadController(Generic[T]):
    def __init__(self, collection_name: str, json_result_file_parser: Strategy) -> None:
        """
        This controller is responsible for download file stored from previous job into the s3 bucket.

        Parameters:
            collection_name - The collection name to refer to for database.
            json_result_file_parser - A strategy for parsing result files into a json to update file names mongodb schema.

        """

        self.cn = collection_name
        self.udc = UDContrl(collection_name, json_result_file_parser)


    def download(self, uuid: str, algorithm: str, type: str, name: str) -> str:
        """
        This controller is responsible for download file stored from previous job into the s3 bucket.

        Parameters:
            collection_name - The collection name to refer to for database.
            json_result_file_parser - A strategy for parsing result files into a json to update file names mongodb schema.

        """

        path = ""
        output = ""

        if algorithm == "gifdroid":
            output = "gifdroid.json"
            path = os.path.join(uuid, algorithm, output)
        elif algorithm == "xbot":
            if type == "issues":

                file_type=".txt"
                output = DownloadController.join_str(name, file_type)

            if type == "images":
                file_type = ".png"
                output = DownloadController.join_str(name, file_type)

            path = os.path.join(uuid, "activity", name, algorithm, type, output)

        elif algorithm == "owleye":

            file_type = ".jpg"
            output = DownloadController.join_str(name, file_type)

            path = os.path.join(uuid, "activity", name, type, output)
        elif algorithm == "activity":
            if type == "images":
                file_type = ".jpg"
                output = DownloadController.join_str(name, file_type)

            path = os.path.join(uuid, "activity", name, type, output)

        print("DOWNLOAD: Downloading file from", os.path.join( "apk-bucket", path ))
        s3_client.download_file(Bucket='apk-bucket', Key=path, Filename=output)

        return output


    @staticmethod
    def join_str(str1: str, str2: str) -> str:
        """
        Join 2 texts together
        """

        return str1 + str2

