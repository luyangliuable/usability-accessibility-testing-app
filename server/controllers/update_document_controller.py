from utility.uuid_generator import unique_id_generator
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from models.DBManager import DBManager
import datetime
import json

from download_parsers.gifdroid_json_parser import gifdroidJsonParser
from download_parsers.strategy import Strategy
from enums.status_enum import StatusEnum


class UpdateDocumentController:
    """
    This controller class is used to update metadata for files on mongodb for traceability purpose.
    """
    def __init__(self, collection_name: str, json_result_file_parser: Strategy):
        ###############################################################################
        #                          Initiate database instance                         #
        # ###############################################################################
        # self.collection_name = "apk"
        self.collection_name = collection_name
        self.mongo = DBManager.instance()

        ###############################################################################
        #                               Update stratefy                               #
        ###############################################################################
        self._strategy = json_result_file_parser

        self.c = self.mongo.get_collection('apk')

        # Attribute lookup for algorithm
        self.lookup = {
            "owleye": "activity",
            "storydisitiller": "activity",
            "xbot": "activity",
            "gifdroid": "gifdroid",
            "droidbot": "gifdroid",
        }


    def get_lookup(self):
        return self.lookup


    def insert_algorithm_result(self, uuid: str, algorithm: str, links_to_res: list, result_type:str, file_names: list):
        """
        This function inserts the links to the algorithm results into the document matching uuid

        Parameters:
            uuid - uuid for the job which is the cluster of algorithms tasked to run
            algorithm - the algorithm the result links for
            links_to_res - the single link to result. NOTE that element in list is dynamically typed so it can be a string

        """


        ###############################################################################
        #                             Convert file to json                            #
        ###############################################################################
        result_key_in_d = "results"

        ###############################################################################
        #   TODO Allow to insert strategy to have different algorithms for parsing    #
        ###############################################################################

        # Get document matching uuid ############################################
        d = self.mongo.get_document(uuid, self.c)

        # Get the results segment #####################################################
        result = d[result_key_in_d]

        # Change document and insert result link ######################################
        prev = result[self.lookup[algorithm]][result_type]
        tmp = self._strategy.do_algorithm(uuid, links_to_res, file_names)
        print(tmp)

        print(result['gifdroid'])
        result[self.lookup[algorithm]][result_type] = prev + tmp

        # Update result back #####################################################
        self.mongo.update_document(uuid, self.c, result_key_in_d, result)

        return result


    def get_document(self, uuid: str):
        """
        Get file metadata that matches the job uuid

        Parameters:
            uuid (str) - The job uuid the identifies the cluster of algorithms to run
        """

        # Get document that match uui in apk colletion #########################
        result = self.mongo.get_document(
            uuid=uuid,
            collection=self.c
        )

        # # The result for mongodb get document returns a list ##########################
        # result = [item for item in result]

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

            self.mongo.insert_document(document, self.c).inserted_id

            return document['uuid'], 200
        except Exception as e:
            ###############################################################################
            #                                Error Handling                               #
            ###############################################################################
            return str(e), 400

