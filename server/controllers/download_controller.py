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

    def download(self,uuid,algorithm, type, name):

        # data = {'uuid': uuid}
        # headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        # response = requests.get('http://docker.host.internal:5005/file/get', data=json.dumps( data ), headers=headers)
        # lookup = get_document(uuid)[0]
        lookup = self.udc.get_document(uuid)

        ###############################################################################
        #      If the file is json just respond with json instead of sendinf file     #
        ###############################################################################

        print(type)
        print(name)
        print(lookup['results'][algorithm][type])

        # try:
        #     result_file_from_algorithm = [o for o in lookup['results'][algorithm][type] if o['name'] == name][0]
        # except:
        #     raise IndexError("File is not stored")

        ###############################################################################
        #                        TODO Update more buckets here                        #
        ###############################################################################


        s3_client.download_file(Bucket='apk-bucket', Key=os.path.join(uuid, name), Filename=name)

        return name
