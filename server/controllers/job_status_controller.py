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
        "name": "{name of activity / screenshot}",
        "image": "{link to screenshot image}",
        "xbot": {
            "image": "{link to xbot screenshot}",
            "description": "{description of issues in screenshot (string)}"
        },
        "owleye": {
            "image": "{link to owleye heatmap screenshot}"
        },
        "tapshoe": {
            "image": "{link to screenshot of tapshoe image}",
            "description": "{string description of image}",
            "heatmap": "{link to heatmap image}"
        },
    }


    _job_status_key = 'overall-status'

    def __init__(self, collection_name: str) -> None:
        ###############################################################################
        #                          Initiate database instance                         #
        ###############################################################################
        self._db = DBManager.instance()
        self.collection = self._db.get_collection(collection_name)

    def get(self, uuid: str) -> str:

        # Get status ##################################################################
        status = d['overall-status']
        status['apk'] = d['apk']

        return status

    def post(self, uuid: str, **kwargs) -> t.Dict[str, str]:
        job_status = self._get_job_status(uuid)

        parameters = [key for key in self._db.get_format('_')[
            'overall-status']]

        for each_parameter in parameters:
            if each_parameter in kwargs:
                updated_attribute = kwargs[each_parameter]

                if each_parameter == 'logs' and updated_attribute != None:
                    self._store_logs(job_status, updated_attribute)

                elif each_parameter == 'progress' and updated_attribute != None:
                    job_status['progress'] += updated_attribute

                else:
                    job_status[each_parameter] = updated_attribute

        self._db.update_document(uuid, self.collection, self._job_status_key, job_status)

        return job_status

    def _get_job_status(self, uuid: str):
        job_status = self._db.get_document(uuid, self.collection)[self._job_status_key]

        return job_status


    def check_algorithm_is_dependency(self, uuid: str, algorithm: str) -> bool:
        algorithm_to_run_key = 'algorithms_to_run'
        return not algorithm in self._db.get_document(uuid, self.collection)[self._job_status_key][algorithm_to_run_key]


    def get_total_number_of_algorithms_in_job(self, uuid: str) -> int:
        job_status = self._get_job_status(uuid);
        return len(job_status['algorithms_to_run'])


    def add_to_algorithm_to_run(self, uuid: str, algorithm: str):
        job_status = self._get_job_status(uuid)

        if self.check_algorithm_is_dependency(uuid, algorithm):
            job_status['algorithms_to_run'].append(algorithm)
            self._db.update_document(uuid, self.collection, self._job_status_key, job_status)

    def _store_logs(self, document: t.Dict[str, t.List], new_log: str) -> bool:
        """
        Stores only the past 10 logs into the **mongodb** document for the job uuid

        Parameters:
            document - (str) The mongodb document for the job uuid
            new_log - (str) New log message
        """
        document['logs'].append(new_log)
        logs_length = len(document['logs'])
        if logs_length > 10:
            document['logs'] = document['logs'][logs_length-10: logs_length]

        return True

    def get_collection(self) -> Collection:
        return self.collection

    def insert(self, uuid: str):
        pass


if __name__ == "__main__":
    pass
