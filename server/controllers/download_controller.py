import boto3
import json
import uuid
import os
from controllers.update_document_controller import UpdateDocumentController as UDContrl
from utility.uuid_generator import unique_id_generator

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
    def __init__(self):
        pass

    def download(self,uuid,algorithm):

        # data = {'uuid': uuid}
        # headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        ud_ctr =  UDContrl()

        # response = requests.get('http://docker.host.internal:5005/file/get', data=json.dumps( data ), headers=headers)
        # lookup = get_document(uuid)[0]
        lookup = ud_ctr.get_document(uuid)

        ###############################################################################
        #      If the file is json just respond with json instead of sendinf file     #
        ###############################################################################
        print(lookup)

        if algorithm == "apk":
            result_file_from_algorithm = lookup[algorithm]['name']
        else:
            result_file_from_algorithm = lookup[algorithm]

        ###############################################################################
        #                        TODO Update more buckets here                        #
        ###############################################################################
        result_bucket = 'apk-bucket'

        if algorithm == 'apk':
            result_bucket = 'apk-bucket'

        print("Getting file from", os.path.join(uuid, result_file_from_algorithm))

        s3_client.download_file(Bucket=result_bucket, Key=os.path.join(uuid, result_file_from_algorithm), Filename=result_file_from_algorithm)

        return result_file_from_algorithm
        # return send_file(result_file_from_algorithm, as_attachment=True), 200
