from controllers.algorithm_data_controller import AlgorithmDataController as ADC
from download_parsers.strategy import Strategy
from typing import TypeVar, Generic
from utility.enforce_bucket_existance import *
from controllers.controller import Controller
import tempfile
import subprocess
import os

T = TypeVar('T')

class DownloadController(Generic[T], Controller):

    bucket_name = 'apk-bucket'

    def __init__(self, collection_name: str, json_result_file_parser: Strategy) -> None:
        """
        This controller is responsible for download file stored from previous job into the s3 bucket.

        Parameters:
            collection_name - The collection name to refer to for database.
            json_result_file_parser - A strategy for parsing result files into a json to update file names mongodb schema.

        """

        self.cn = collection_name
        self.adc = ADC(collection_name, json_result_file_parser)


    def get(self, uuid: str, algorithm: str, type: str, name: str) -> str:
        """
        This controller is responsible for download file stored from previous job into the s3 bucket.

        Parameters:
            collection_name - The collection name to refer to for database.
            json_result_file_parser - A strategy for parsing result files into a json to update file names mongodb schema.


        Gifdroid files are stored in:
            - /
                - gifdroid/

        xbot images files are stored in:
            - /
                - activity/{ screen_name }/xbot/images/

        xbot issues files are stored in:
            - /
                - activity/{ screen_name }/xbot/issues/

        tappable issues files are stored in:
            - /
                - activity/{ screen_name }/tappable/
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
            path = os.path.join(uuid, "activity", name, algorithm, output)

        elif algorithm == "activity":

            if type == "images":
                file_type = ".png"
                output = DownloadController.join_str(name, file_type)

            path = os.path.join(uuid, "activity", name, type, output)

        print(f'DOWNLOAD: Downloading file from { os.path.join( "apk-bucket", path ) }')

        s3_client.download_file(Bucket='apk-bucket', Key=path, Filename=output)

        return output


    def download_all_objects_in_folder(self, uuid: str) -> str:
        """
        Gets all the files out of folder on s3 bucket matching uuid for user to download

        Parameters:
            uuid - str that matches with the job uuid to get a full summary of the job

        Returns: str Path leading to stored summary location.
        """

        with tempfile.TemporaryDirectory() as sys_tmp_folder:
            cwd = os.getcwd()
            local_tmp_save_dir = tempfile.mkdtemp(dir=cwd)
            print(ENDPOINT_URL)
            subprocess.run(['aws', f'--endpoint-url={ENDPOINT_URL}', 's3', 'cp', f's3://{BUCKETNAME}/{uuid}/', local_tmp_save_dir, '--recursive'])

        return local_tmp_save_dir


    def post(self, uuid: str, **kwargs):
        pass


    @staticmethod
    def join_str(str1: str, str2: str) -> str:
        """
        Join 2 texts together
        """

        return str1 + str2
