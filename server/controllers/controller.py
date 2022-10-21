from pymongo.database import Collection
from models.DBManager import DBManager
from abc import ABC, abstractmethod
import boto3
import os

###############################################################################
#                                  Set Up AWS                                 #
###############################################################################
AWS_PROFILE = 'localstack'
AWS_REGION = 'us-west-2'
ENDPOINT_URL = os.environ.get('S3_URL')
BUCKETNAME = "apk-bucket"

class Controller(ABC):
    def __init__(self, collection_name: str):

        """
        The controller is responsible for controlling the backend.

        Parameters:
            collection_name - The collection name to refer to for database.
            json_result_file_parser - A strategy for parsing result files into a json to update file names mongodb schema.

        Variables:
            self.cn - The mongodb collection name
            self._strategy - strategy for parsing the algorithm metadata into mongodb schema format
            self.c - (Collection) The collection object from mongodb
            self.s3_client - The client for dealing with virtual local aw3 bucket from localstack
        """

        self.cn = collection_name
        self._db = DBManager.instance()
        self.c = self._db.get_collection('apk')

        boto3.setup_default_session(profile_name=AWS_PROFILE)
        self.s3_client = boto3.client(
            "s3",
            region_name=AWS_REGION,
            endpoint_url=ENDPOINT_URL
        )

    def get_collection(self) -> Collection:
        return self.c

    @abstractmethod
    def get(self, uuid: str, **kwargs):
        pass


    @abstractmethod
    def post(self, uuid: str, **kwargs):
        pass
