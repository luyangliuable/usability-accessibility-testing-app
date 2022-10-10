from utility.uuid_generator import unique_id_generator
from utility.enforce_bucket_existance import *
from controllers.controller import Controller
from models.DBManager import DBManager
import typing as t
import os


T = t.TypeVar('T')


class UploadController(t.Generic[T], Controller):

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
        self.save_dir = "/home/data"


    def get(self, uuid: str) -> str:
        """
        Get the save directory of the uploaded files

        Parameters:
            uuid - (str) The unique id of the job identifying all the algorithms
        """
        return os.path.join(self.save_dir, uuid)


    def post(self, files: 'werkzeug.datastructures.ImmutableMultiDict') -> t.Dict[str, T]:
        """
        Upload the files by saving them to /home/data for now.

        Parameters:
            files - (ImmutableMultiDict) Dictionary of files uploaded by the user

        Returns: The mongodb schema to by inserted in the future containing the information about the files.
        """
        uuid = unique_id_generator()
        data = self._get_format(uuid)

        output_path = os.path.join(self.save_dir, uuid)
        os.mkdir(output_path)

        self._save_additional_files(uuid, files, data)
        self._save_apk_file(uuid, files, data)

        self.acknowlege(uuid, data)

        return data


    def _get_format(self, uuid: str) -> t.Dict[str, T]:
        """
        Get the mongodb schema or json format.

        Parameters:
            uuid - (str) The unique id for the job

        Returns: The mongodb schema to by inserted in the future containing the information about the files.
        """
        data = DBManager.get_format(uuid)

        return data


    def _save_additional_files(self, uuid: str, files: 'werkzeug.datastructures.ImmutableMultiDict', data: t.Dict[str, T]) -> t.Dict[str, T]:
        """
        Save one apk file uploaded by the user.

        Parameters:
            files - (ImmutableMultiDict) Dictionary of files uploaded by the user
            data - (Dict) The mongodb schema to by inserted in the future containing the information about the files.

        Returns: The mongodb schema to by inserted in the future containing the information about the files.
        """
        additional_files_bucket_folder = "additional files"

        for key, item in files.items():
            if key != "apk_file":
                print(f'{additional_files_bucket_folder} { item.name } detected,')

                temp_directory_name = os.path.join(self.save_dir, uuid, item.name)
                self._create_directory(temp_directory_name)
                temp_file_name = os.path.join(temp_directory_name, item.filename)

                with open(temp_file_name, "wb") as savefile:
                    savefile.write(item.read())
                    savefile.close()

                s3_client.upload_file(temp_file_name, BUCKETNAME, os.path.join( uuid, additional_files_bucket_folder, item.filename ))

                data["additional_files"].append({"algorithm": item.name, "type": item.content_type, "name": item.filename, "notes": ""})

        return data


    def _create_directory(self, directory: str) -> None:
        if not os.path.exists(directory):
            os.makedirs(directory)


    def _save_apk_file(self, uuid: str, files: 'werkzeug.datastructures.ImmutableMultiDict', data: t.Dict[str, T]) -> str:
        """
        Save one apk file uploaded by the user.

        Parameters:
            files - (ImmutableMultiDict) Dictionary of files uploaded by the user
            data - (Dict) The mongodb schema to by inserted in the future containing the information about the files.

        Returns: String of the apk file name
        """


        apk_file = files['apk_file']
        apk_filename = apk_file.filename
        temp_file_name = os.path.join(self.save_dir, uuid, apk_filename)


        # File name is the original uploaded file name ################################
        apk_file_note = "user uploaded apk file"

        data['apk'] = {"type": "apk", "name": apk_filename, "notes": apk_file_note}

        ###############################################################################
        #                Create a temporary file to store file content                #
        ###############################################################################
        with open(temp_file_name, "wb") as savefile:
            savefile.write(apk_file.read())
            savefile.close()

        return apk_filename


    def acknowlege(self, uuid: str, data: t.Dict[str, str]) -> bool:
        """
        After uploaded, this function updates the mongodb schema and uploads the file to s3 bucket as well.

        Parameters:
            files - (ImmutableMultiDict) Dictionary of files uploaded by the user
            data - (Dict) The mongodb schema to by inserted in the future containing the information about the files.

        Returns: boolean indicating if the function executed successfully
        """
        temp_file_name = os.path.join(self.save_dir, uuid, data['apk']['name'])

        apk_bucket_folder = "apk"

        s3_client.upload_file(
            temp_file_name,
            BUCKETNAME,
            os.path.join( uuid, apk_bucket_folder, data['apk']['name'] )
        )

        self._db.insert_document(data, self._db.get_collection('apk'))

        return True
