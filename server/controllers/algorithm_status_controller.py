# from __future__ import annotations
from controllers.controller import Controller
import typing as t
from typing import TypeVar, Generic, Dict
from enums.status_enum import StatusEnum
from models.DBManager import DBManager


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


    def __init__(self, collection_name: str) -> None:
        """
        This controller is responsible for controlling **ONE** algorithm status metadata only.

        Parameters:
            collection_name - The collection name to refer to for database.
        """
        self._db = DBManager.instance()
        self.c = self._db.get_collection(collection_name)

        self.status_key = 'algorithm_status'


    def get(self, uuid: str, algorithm: str) -> str:
        """
        Get the status of a specific algorithm
        """
        all_algorithm_status = self._db.get_document(uuid, self.c)
        specific_algorithm_status = all_algorithm_status[self.status_key][algorithm]

        return specific_algorithm_status


    def post(self, uuid: str, algorithm: str, **kwargs) -> t.Dict[str, T]:
        """
        Update the status of a specific algorithm.
        """

        document = self._db.get_document(uuid, self.c)

        status = document[self.status_key]

        viable_parameters = [key for key in self._db.get_format("")['overall-status']]
        for each_parameter in viable_parameters:
            if each_parameter in kwargs:
                if each_parameter == 'logs':
                    """
                    If the parameter is a log, append to all existing logs.
                    """

                    status[algorithm]['logs'].append(kwargs[each_parameter])

                elif each_parameter == 'progress':
                    """
                    If the parameter is a progress integer, add to exiting progress integer.
                    """

                    status[algorithm]['progress'] += kwargs[each_parameter]

                else:
                    status[algorithm][each_parameter] = kwargs[each_parameter]

        self._db.update_document(uuid, self.c, self.status_key, status)

        return document


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

        document = self._db.get_document(uuid, self.c)
        document[self.status_key][algorithm][attribute_key] = attribute_val

        self._db.update_document(uuid, self.c, self.status_key, document[self.status_key])

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
        d = self._db.get_document(uuid, self.c)

        for _, item in d[self.status_key].items():
            item['apk']= apk_name

        self._db.update_document(uuid, self.c, self.status_key, d[self.status_key])

        return d[ self.status_key ]



    def insert(self, uuid: str, **kwargs):
        pass


if __name__ == "__main__":
    pass
