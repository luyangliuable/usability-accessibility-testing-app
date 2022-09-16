import pymongo
from pymongo.database import Collection
import datetime
import json
import os


class DBManager:
    """
        This class is a *singleton* that provides a global access point for API in this project. It access the api key inside .env file. It must be initiated to be used and only one instance can exist at a time
    """

    _instance = None  # _ means it is private

    # https://www.mongodb.com/docs/manual/reference/bson-types/

    def __init__(self):
        """
        NOTE: DO NOT ALLOW initiation directly
        """
        raise RuntimeError(
            'Cannot initialise an api singleton, call instance() instead')

    @staticmethod
    def get_format(uuid: str) -> dict:
        """
        Get the format/model of the data document to be added to model db.

        Parameters:
            uuid (str): The algorthm cluster or job uuid

        Returns:
            data: The model to create a document
        """

        date = datetime.datetime.utcnow().isoformat()

        ###############################################################################
        #               Store data into mongodb in the following format               #
        ###############################################################################

        # uuid - used to identify the cluster of data for one task.
        # date - just the data initiated the task
        # apk - the apk file to analyse
        # tapshoe_files - store tapeshoe files here
        # storydistiller_files - store storydistiller files here
        # gifdroid_files - store gifdroid files here
        # utg_files - store droidbot files here
        # venus_files - store venus files here

        # NOTE: store in the following format for files for easier identifcation
        # {"type": {The file/mime type}, "name": {Name of file inside s3 bucket}, "notes": "Notes to take into consideration"}

        data = {
            "uuid": uuid,
            "date": date,
            "apk": {
                "type": "",
                "name": "",
                "s3_bucket": "",
                "s3_key": "",
            },
            "additional_files": [],
            "overall_status": {
                "status": "",
                "percentage": 0,
                "logs": [],
            },
            "algorithm_status": {
                "storydistiller": {
                    "status": "",
                    "notes": "",
                    "start_time": "",
                    "end_time": "",
                    "apk": ""
                },
                "owleye": {
                    "status": "",
                    "notes": "",
                    "start_time": "",
                    "end_time": "",
                    "apk": ""
                },
                "xbot": {
                    "status": "",
                    "notes": "",
                    "start_time": "",
                    "end_time": "",
                    "apk": ""
                },
                "gifdroid": {
                    "status": "",
                    "notes": "",
                    "start_time": "",
                    "end_time": "",
                    "apk": ""
                },
                "ui_checker": {
                    "status": "",
                    "notes": "",
                    "start_time": "",
                    "end_time": "",
                    "apk": ""
                }
            },
            "algorithm_outputs": {
                "storydistiller": "",
                "xbot": ""
            },
            "results": {
                "activities": [
                    {
                        "name": "",
                        "image": [],
                        "xbot": {
                            "image": "",
                            "description": ""
                        },
                        "owleye": {
                            "image": []
                        },
                        "tapshoe": {
                            "image": [],
                            "description": "",
                            "heatmap": "{link to heatmap image}"
                        }
                    }
                ],
                "gifdroid": {
                    "images": [],
                    "json": []
                },
                "uichecker": {}
            }
        }

        # with open("document_format.json", "r") as f:
        #     data = json.load(f)

        data['uuid'] = uuid
        data['date'] = datetime.datetime.now()

        return data

    @classmethod
    def instance(cls):
        """
        If there is already an instance, just return the single instance. Otherwise create a new instance of api.
        """
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls.url = os.environ.get('MONGO_URL')
            cls.connect()
            cls.db = None

        return cls._instance

    def get_document(self, uuid: str, collection: Collection):
        cursor = collection.find({"uuid": uuid})

        result = []
        for document in cursor:
            # Find document that match with current uuid.
            if document["uuid"] == uuid:
                # utg_filename = document['utg_files']
                result.append(document)

        # Assume only 1 result
        return result[0]

    @classmethod
    def get_db_status(cls, db_name: str):
        try:
            client = pymongo.MongoClient(cls.url)
            exec("%s%s" % ("client.", db_name))
        except:
            return False
        else:
            return True

    def get_database(self):
        return self._db

    @staticmethod
    def create_mongo_validator(user_schema: dict):
        required = []
        validator = {'$jsonSchema': {'bsonType': 'object', 'properties': {}}}

        # Bson types
        # https://www.mongodb.com/docs/manual/reference/bson-types/

        for field_key in user_schema:
            field = user_schema[field_key]
            properties = {'bsonType': field['type']}
            minimum = field.get('minlength')

            if type(minimum) == int:
                properties['minimum'] = minimum

            if field.get('required') is True:
                required.append(field_key)

            validator['$jsonSchema']['properties'][field_key] = properties

        return validator

    def create_collection(self, collection_name: str, schema=None):
        validator = {}

        if schema != None:
            validator = DBManager.create_mongo_validator(schema)

        # Placeholder result variable
        result = Collection(self._db, collection_name)

        try:
            result = self._db.create_collection(
                collection_name, validator=validator)
        except Exception as e:
            # Collection may already exist
            print(e)
        else:
            print("Collection", collection_name, "created")

        return result

    def update_document(self, uuid: str, collection: Collection, attribute: str, value):

        collection.update_one(
            {
                "uuid": uuid
            },
            {
                "$set": {
                    attribute: value
                }
            }
        )

    def get_collection(self, collection_name: str):
        return self._db.get_collection(collection_name)

    def insert_document(self, document, collection: Collection):
        post_id = collection.insert_one(document)

        print(post_id)

        return post_id

    @classmethod
    def connect(cls):
        try:
            cls.connection = pymongo.MongoClient(cls.url)
            cls._db = cls.connection.fit3170
            cls.connection.server_info()  # Triger exception if connection fails to the database
        except Exception as ex:
            print('failed to connect DBManager', ex)
        else:
            print("Successfully connected to mongodb.")


if __name__ == "__main__":
    pass
