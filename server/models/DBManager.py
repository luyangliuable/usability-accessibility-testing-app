import pymongo
from pymongo.database import Collection
import os

class DBManager:
    """
        This class is a *singleton* that provides a global access point for API in this project. It access the api key inside .env file. It must be initiated to be used and only one instance can exist at a time
    """

    _instance = None  # _ means it is private

    def __init__(self):
        """
        NOTE: DO NOT ALLOW initiation directly
        """
        raise RuntimeError('Cannot initialise an api singleton, call instance() instead')


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


    def get_document(self, uuid: str, collection: str = 'apk'):
        cursor = self._db[collection].find({"uuid": uuid})

        result = []
        for document in cursor:
            # Find document that match with current uuid.
            if document["uuid"] == uuid:
                # utg_filename = document['utg_files']
                result.append(document)

        return result


    def get_database(self):
        return self._db

    def create_collection(self, collection_name: str):
        self.collection = exec("%s%s" % ( "self._db.", collection_name ) )
        print("Collection", collection_name, "created")


    def get_collection(self, collection_name:str):
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
            print("Successfully connected to mongodb. DBManager")
