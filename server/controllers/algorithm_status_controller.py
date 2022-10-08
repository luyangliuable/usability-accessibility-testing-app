# from __future__ import annotations
from controllers.controller import Controller
from controllers.job_status_controller import JobStatusController
from typing import TypeVar, Generic, Dict
from enums.status_enum import StatusEnum
from models.DBManager import DBManager
from datetime import datetime as dt
import typing as t


T = TypeVar('T')


class AlgorithmStatusController(Generic[T], Controller):
    """
        This controller is responsible for controlling **ONE** algorithm status metadata only.

        Updates algorithm_status. Gets algorithm_status.
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

    status_key = 'algorithm_status'

    def __init__(self, collection_name: str) -> None:
        """
        This controller is responsible for controlling **ONE** algorithm status metadata only.

        Parameters:
            collection_name - The collection name to refer to for database.
        """
        self.job_status_controller = JobStatusController(collection_name)
        self._db = DBManager.instance()
        self.collection = self._db.get_collection(collection_name)


    def get(self, uuid: str, algorithm: str) -> str:
        """
        Get the status of a specific algorithm
        """
        all_algorithm_status = self._db.get_document(uuid, self.collection)
        specific_algorithm_status = all_algorithm_status[self.status_key][algorithm]
        print(specific_algorithm_status)

        return specific_algorithm_status


    def post(self, uuid: str, algorithm: str, **kwargs) -> t.Dict[str, T]:
        """
        Update the status of a specific algorithm.
        """

        all_algorithm_status = self._get_all_algorithm_status(uuid)
        self._inject_updated_status_info_into_document(all_algorithm_status, algorithm, **kwargs)
        self._db.update_document(uuid, self.collection, self.status_key, all_algorithm_status)
        self._reflect_algorithm_update_to_job(uuid, algorithm, **kwargs)

        return all_algorithm_status[algorithm]


    def _reflect_algorithm_update_to_job(self, uuid: str, algorithm: str, **kwargs) -> None:
        """
        This is necessary Because when an algorithm updates, the job progress and logs changes as well for the frontend to see.
        """

        self.job_status_controller.add_to_algorithm_to_run(uuid, algorithm)
        self.job_status_controller.post(uuid, logs=kwargs['logs'])

        if 'status' in kwargs:
            total_number_of_algorithms_to_execute = self.job_status_controller.get_total_number_of_algorithms_in_job(uuid)
            if kwargs['status'] == StatusEnum.running.value or kwargs['status'] == StatusEnum.successful.value:
                self.job_status_controller.post(uuid, progress=(0.5/total_number_of_algorithms_to_execute)*100)


    def _inject_updated_status_info_into_document(self, all_algorithm_status: t.Dict, algorithm, **kwargs) -> t.Dict[str, T]:
        viable_parameters = [key for key in self._db.get_format("")[self.status_key][algorithm]]

        for each_parameter in viable_parameters:
            if each_parameter in kwargs:
                if each_parameter == 'logs' and kwargs[each_parameter] != None:
                    """
                    If the parameter is a log, append to all existing logs.
                    """
                    self._store_logs(all_algorithm_status, algorithm, kwargs[each_parameter])

                elif each_parameter == 'progress' and kwargs[each_parameter] != None:
                    """
                    If the parameter is a progress integer, add to exiting progress integer.
                    """

                    all_algorithm_status[algorithm]['progress'] += kwargs[each_parameter]

                elif each_parameter == 'status' and kwargs[each_parameter] != None:
                    status = kwargs[each_parameter]
                    if status == StatusEnum.running.value:
                        print(f'Updating start time into {all_algorithm_status[algorithm]}.')
                        all_algorithm_status[algorithm]['start_time'] = str( dt.now() )
                    elif status == StatusEnum.successful.value:
                        all_algorithm_status[algorithm]['end_time'] = str( dt.now() )
                    all_algorithm_status[algorithm][each_parameter] = kwargs[each_parameter]
                else:
                    all_algorithm_status[algorithm][each_parameter] = kwargs[each_parameter]

        return all_algorithm_status


    def _get_all_algorithm_status(self, uuid: str) -> t.Dict[str, t.Dict[str, T]]:
        """
        Get all specific algorithm status information such as start time, state and logs etc.

        Parameters:
            uuid - (str) The unique id of the job (including all algorithms).
            algorithms - (str) The algorithm (e.g. gifdroid, storydistiller, owleye, xbot, tappable etc)

        Returns: The status dictionary/json containing all data on the status of the algorithm.
        """
        return self._db.get_document(uuid, self.collection)[self.status_key]



    def _store_logs(self, document: t.Dict[str, t.Dict[str, t.List ]], algorithm: str, new_log: str) -> bool:
        """
        Stores only the past 10 logs into the **mongodb** document for the algorithm

        Updating algorithm log also updates job log.

        Parameters:
            document - (str) The mongodb document for the job uuid
            new_log - (str) New log message
        """
        log_key = 'logs'
        max_logs = 10
        document[algorithm][log_key].append(new_log)
        logs_length = len(document[algorithm][log_key])
        if logs_length > max_logs:
            document[algorithm][log_key] = document[algorithm][log_key][logs_length-10: logs_length]

        return True


    def update_status_attribute(self, uuid: str, algorithm: str, attribute_key: str, attribute_val: str) -> t.Dict[str, T]:
        """
        Update a specific algorithm status attribute on **mongodb**.

        This is useful because you don't have to repeat a lot of lines of code.

        Parameters:
            uuid - (str) job uuid
            algorithm - (str) algorithm name
            key - (str) attribute key
            val - (str) new attribute value
        """

        document = self._db.get_document(uuid, self.collection)
        document[self.status_key][algorithm][attribute_key] = attribute_val

        self._db.update_document(uuid, self.collection, self.status_key, document[self.status_key])

        return document


    def update_apk_filename(self, uuid: str, algorithm: str, apk_filename: str):
        """
        Update the apk name for the algorithm's process on **mongodb**

        Parameters:
            uuid - (str) job uuid
            algorithm - (str) the algorithm to update for on mongodb
            apk_filename - (str) the apk_filename to update to
        """

        key = "apk"
        return self.update_status_attribute(uuid, algorithm, key, apk_filename)



    def declare_apk_name_in_status(self, uuid: str, apk_name: str) -> Dict[str, str]:
        """
        Ignore please but don't delete yet
        """
        d = self._db.get_document(uuid, self.collection)

        for _, item in d[self.status_key].items():
            item['apk']= apk_name

        self._db.update_document(uuid, self.collection, self.status_key, d[self.status_key])

        return d[ self.status_key ]



    def insert(self, uuid: str, **kwargs):
        pass


if __name__ == "__main__":
    pass
