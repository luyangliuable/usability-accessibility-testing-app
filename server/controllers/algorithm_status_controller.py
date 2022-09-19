# from __future__ import annotations
from typing import TypeVar, Generic, List, Callable, Dict
from enums.algorithm_enum import AlgorithmEnum as Algorithm
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from models.DBManager import DBManager
from enums.result_types import ResultTypeEnum
from typing import List
from download_parsers.gifdroid_json_parser import gifdroidJsonParser
from download_parsers.strategy import Strategy
from pymongo import database
from pymongo.database import Collection


from enums.status_enum import StatusEnum

T = TypeVar('T')

class AlgorithmStatusController(Generic[T]):
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


    def __init__(self, collection_name: str) -> None:
        ###############################################################################
        #                          Initiate database instance                         #
        ###############################################################################
        self._db = DBManager.instance()
        self.c = self._db.get_collection(collection_name)


    def get_all_algorithm_status(self, uuid: str) -> Dict[str, str]:

        # Get document ################################################################
        d = self._db.get_document(uuid, self.c)

        # Get status ##################################################################
        s = d['algorithm_status']
        return s


    def decalare_apk_name_in_status(self, uuid: str, apk_name: str) -> Dict[str, str]:
        d = self._db.get_document(uuid, self.c)

        algorithm_status_key = 'algorithm_status'

        for _, item in d[algorithm_status_key].items():
            item['apk']= apk_name

        self._db.update_document(uuid, self.c, algorithm_status_key, d[algorithm_status_key])

        return d[ algorithm_status_key ]


    def get_job_status(self, uuid: str) -> str:
        # Get document ################################################################
        d = self._db.get_document(uuid, self.c)

        # Get status ##################################################################
        status = d['status']

        return status


    def update_job_status(self, uuid: str, status: str) -> None:
        # Get document ################################################################
        d = self._db.get_document(uuid, self.c)

        # Get status ##################################################################

        self._db.update_document(uuid, self.c, 'status', status)

        return self._db.get_document(uuid, self.c)['status']


    def get_collection(self) -> Collection:
        return self.c


    def update_algorthm_status_apk_file_name(self, uuid: str, algorithm: str, status: str):

        key = "apk"

        return self.update_algorithm_status_attribute(uuid, algorithm, key, status)


    def get_specific_algorithm_status(self, uuid: str, algorithm: str) -> str:
        all_algorithm_status = self.get_all_algorithm_status(uuid)

        specific_algorithm_status = all_algorithm_status[algorithm]

        return specific_algorithm_status


    def update_algorithm_status_attribute(self, uuid: str, algorithm: str, key: str, val: T):
        # Get document ################################################################
        try:
            d = self._db.get_document(uuid, self.c)

            status_key = 'algorithm_status'

            d[status_key][algorithm][key] = val

            # Get status ##################################################################
            self._db.update_document(uuid, self.c, status_key, d[status_key])

        except Exception as e:
            print(e)
        else:
            return d


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
