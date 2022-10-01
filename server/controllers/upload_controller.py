from utility.uuid_generator import *
from models.DBManager import *
import typing as t
import tempfile
import boto3
import os


###############################################################################
#                                  Set Up AWS                                 #
###############################################################################
AWS_PROFILE = 'localstack'
AWS_REGION = 'us-west-2'
ENDPOINT_URL = os.environ['S3_URL']
print(ENDPOINT_URL)
BUCKETNAME = "apk-bucket"


boto3.setup_default_session(profile_name=AWS_PROFILE)

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    endpoint_url=ENDPOINT_URL
)

T = t.TypeVar('T')

class UploadController(t.Generic[T]):

    bucket_name = 'apk-bucket'

    def __init__(self, collection_name: str) -> None:
        """
        This controller is responsible for download file stored from previous job into the s3 bucket.

        Parameters:
            collection_name - The collection name to refer to for database.
            json_result_file_parser - A strategy for parsing result files into a json to update file names mongodb schema.

        """

        self.cn = collection_name
        self._db = DBManager.instance()
        self.temp_dir = "/home/data"

    def _get_format(self, uuid: str) -> t.Dict[str, T]:
        # Document template to be inserted into mongodb
        data = DBManager.get_format(uuid)

        return data


    def upload(self, files: 'werkzeug.datastructures.ImmutableMultiDict') -> t.Dict[str, T]:
        ###############################################################################
        #                              Generate unique id                             #
        ###############################################################################
        uuid = unique_id_generator()
        data = self._get_format(uuid)

        output_path = os.path.join(self.temp_dir, uuid)
        os.mkdir(output_path)

        self.save_additional_files(uuid, files, data)
        self.save_apk_file(uuid, files, data)

        self.acknowlege(uuid, data)

        return data


    def save_additional_files(self, uuid: str, files: 'werkzeug.datastructures.ImmutableMultiDict', data: t.Dict[str, T]) -> t.Dict[str, T]:
        ###############################################################################
        #                         S3: Save every additional file                      #
        ###############################################################################
        additional_files_bucket_folder = "additional files"

        for key, item in files.items():
            if key != "apk_file":
                print(f'{additional_files_bucket_folder} { item.name } detected,')

                temp_file_name = os.path.join(self.temp_dir, uuid, str( item.name ))

                with open(temp_file_name, "wb") as savefile:
                    savefile.write(item.read())
                    savefile.close()

                s3_client.upload_file(temp_file_name, BUCKETNAME, os.path.join( uuid, additional_files_bucket_folder, item.filename ))

                data["additional_files"].append({"algorithm": item.name, "type": item.content_type, "name": item.filename, "notes": ""})

        return data


    def save_apk_file(self, uuid: str, files: 'werkzeug.datastructures.ImmutableMultiDict', data: t.Dict[str, T]) -> str:
        ###############################################################################
        #                Create a temporary file to store file content                #
        ###############################################################################
        print("[2] Generating apk file")

        apk_file = files['apk_file']
        apk_filename = apk_file.filename
        temp_file_name = os.path.join(self.temp_dir, uuid, apk_filename)


        # File name is the original uploaded file name ################################

        apk_file_note = "user uploaded apk file"

        # WARNING: Changes now apk attribute only has one apk not array.
        data['apk'] = {"type": "apk", "name": apk_filename, "notes": apk_file_note}

        with open(temp_file_name, "wb") as savefile:
            savefile.write(apk_file.read())
            savefile.close()

        return apk_filename


    def acknowlege(self, uuid: str, data: t.Dict[str, str]) -> bool:
        temp_file_name = os.path.join(self.temp_dir, uuid, data['apk']['name'])

        apk_bucket_folder = "apk"

        s3_client.upload_file(
            temp_file_name,
            BUCKETNAME,
            os.path.join( uuid, apk_bucket_folder, data['apk']['name'] )
        )

        self._db.insert_document(data, self._db.get_collection('apk'))

        return True


