from utility.uuid_generator import unique_id_generator
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from models.Apk import ApkManager
import datetime
import json

###############################################################################
#                                    Schema                                   #
###############################################################################
data = {
    "uuid": None,
    "date": str( datetime.datetime.now() ),
    "apk": [],
    "additional_files": [],
    "tapshoe_files": [],
    "storydistiller_files": [],
    "gifdroid_files": [],
    "utg_files": [],
    "owleye_files": [],
    "venus_files": [],
}


# @file_blueprint.route("/file", methods=['GET'])
# @cross_origin()
# def check_health():
#     """
#     Method file controller files and submiting CRUD/REST API requests into
#     """

#     return "Working", 200


class FileController:
    """
    This controller class is used to update metadata for files on mongodb for traceability purpose.
    """
    def __init__(self):
        ###############################################################################
        #                          Initiate database instance                         #
        ###############################################################################
        self.collection_name = "apk"
        self.mongo = ApkManager.instance()

        self.collection = self.mongo.get_collection('apk')


    def get_document(self, uuid: str):
        """
        Get file metadata that matches the job uuid

        Parameters:
            uuid (str) - The job uuid the identifies the cluster of algorithms to run
        """

        # Get document that match uui in apk colletion #########################
        result = self.mongo.get_document(
            uuid=uuid,
            collection=self.collection
        )

        # The result for mongodb get document returns a list ##########################
        result = [item for item in result][0]

        return result


    def add_document(self, request_parameters: list):
        """
        Add file metadata that matches the job uuid


        Parameters:
            request_parameters - request parameters that contain contents of document
        """

        try:
            ###############################################################################
            #                         Add file metadata to mongodb                        #
            ###############################################################################

            document = data

            for each_key, _ in document.items():
                document[each_key] = request_parameters.get(each_key)

            document['uuid'] = unique_id_generator()

            self.mongo.insert_document(document, self.collection).inserted_id

            return document['uuid'], 200
        except Exception as e:
            ###############################################################################
            #                                Error Handling                               #
            ###############################################################################
            return str(e), 400

