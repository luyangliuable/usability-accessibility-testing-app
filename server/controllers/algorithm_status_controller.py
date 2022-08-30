# from __future__ import annotations
from typing import TypeVar
from enums.algorithm_enum import AlgorithmEnum as Algorithm
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from models.DBManager import DBManager
from enums.result_types import ResultTypeEnum
from typing import List
from download_parsers.gifdroid_json_parser import gifdroidJsonParser
from download_parsers.strategy import Strategy
import os
import datetime
import json


from enums.status_enum import StatusEnum

# from models.Apk import DBManager

###############################################################################
#    @Trevin insert your strategy for parsing owleye/xbot/story files here    #
###############################################################################


class AlgorithmStatusController():
    """
        Updates algorithm_status. Gets algorithm_status
    """

    activity_result_file_json_format = {
        "name" : "{name of activity / screenshot}",
        "image" : "{link to screenshot image}",
        "xbot" : {
            "image" : "{link to xbot screenshot}",
            "description" : "{description of issues in screenshot (string)}"
        },
        "owleye" : {
            "image" : "{link to owleye heatmap screenshot}"
        },
        "tapshoe" : {
            "image" : "{link to screenshot of tapshoe image}",
            "description" : "{string description of image}",
            "heatmap" : "{link to heatmap image}"
        },
    }


    def __init__(self, collection_name:str, json_result_file_parser: Strategy):
        ###############################################################################
        #                          Initiate database instance                         #
        ###############################################################################
        self._db = DBManager.instance()
        self.c = self._db.get_collection(collection_name)
        self._strategy = json_result_file_parser

        self._json_result_file_parser = json_result_file_parser


    def strategy(self, strategy: Strategy) -> None:
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """

        self._strategy = strategy


    def get_algorithm_status(self, uuid: str):

        # Get document ################################################################
        d = self._db.get_document(uuid, self.c)

        try:
            d = d[0]

            # Get status ##################################################################
            s = d['algorithm_status']
        except Exception as e:
            print(e)
            # exit(1)
        else:
            return s


    def get_colletion(self):
        return self.c


    def update_algorithm_status_attribute(self, uuid: str, algorithm: str, key: str, val):
        # Get document ################################################################
        try:
            d = self._db.get_document(uuid, self.c)
            d = d[0]

            status_key = 'algorithm_status'

            d[status_key][algorithm][key] = val

            # Get status ##################################################################
            self._db.update_document(uuid, self.c, status_key, d[status_key])

        except Exception as e:
            print(e)
        else:
            return d

    def insert_algorithm_result(self, uuid: str, algorithm: str, links_to_res: list, result_type:str):
        """
        This function inserts the links to the algorithm results into the document matching uuid

        Parameters:
            uuid - uuid for the job which is the cluster of algorithms tasked to run
            algorithm - the algorithm the result links for
            links_to_res - the single link to result. NOTE that element in list is dynamically typed so it can be a string

        """

        # Attribute lookup for algorithm
        lookup = {
            "owleye": "activity",
            "storydisitiller": "activity",
            "xbot": "activity",
            "gifdroid": "gifdroid",
            "droidbot": "gifdroid",
        }

        ###############################################################################
        #                             Convert file to json                            #
        ###############################################################################

        result_key_in_d = "results"

        ###############################################################################
        #   TODO Allow to insert strategy to have different algorithms for parsing    #
        ###############################################################################

        # Get document matching uuid ############################################
        d = self._db.get_document(uuid, self.c)

        # Get the results segment #####################################################
        result = d[result_key_in_d]

        # Change document and insert result link ######################################
        prev = result[lookup[algorithm]][result_type]
        tmp = self._strategy.do_algorithm(uuid, links_to_res)
        result[lookup[algorithm]][result_type] = prev + tmp

        # Update result back #####################################################
        self._db.update_document(uuid, self.c, result_key_in_d, result)

        return result


    def update_algorithm_status(self, uuid: str, algorithm: str, new_status: str):
        # Get document ################################################################

        try:
            d = self._db.get_document(uuid, self.c)

            status_key = 'algorithm_status'

            status = d[status_key]

            status[algorithm]['status'] = new_status # TODO find a way here to use StatusEnum

            # Get status ##################################################################

            self._db.update_document(uuid, self.c, status_key, status)

        except Exception as e:
            print(e)
        else:
            return status





if __name__ == "__main__":
    pass
