# from __future__ import annotations
import typing as t
from models.DBManager import DBManager
from pymongo.database import Collection
from controllers.controller import Controller
from datetime import datetime

from enums.status_enum import StatusEnum

T = t.TypeVar('T')

class JobStatusController(t.Generic[T], Controller):
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


    def get(self, uuid: str) -> str:
        # Get document ################################################################
        d = self._db.get_document(uuid, self.c)

        # Get status ##################################################################
        status = d['overall-status']

        return status


    def update(self, uuid: str, **kwargs) -> t.Dict[str, str]:
        # Get document ################################################################
        job_status_key = 'overall-status'

        d = self._db.get_document(uuid, self.c)[job_status_key]

        parameters = [key for key in self._db.get_format("")['overall-status']]

        for p in parameters:
            if p in kwargs:
                if p == 'logs':
                    d['logs'].append(kwargs[p])
                elif p == 'progress':
                    d['progress'] += kwargs[p]
                else:
                    d[p] = kwargs[p]

        self._db.update_document(uuid, self.c, job_status_key, d)

        return d


    def get_collection(self) -> Collection:
        return self.c


    def insert(self, uuid: str):
        pass


    def post(self, uuid: str):
        pass

if __name__ == "__main__":
    pass
