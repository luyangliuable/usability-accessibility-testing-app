from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import datetime
import json
import uuid
from models.Apk import ApkManager
from enums.algorithm_enum import AlgorithmEnum as Algorithm

# from models.Apk import ApkManager

class algorithm_status_controller():
    """
        Updates algorithm_status. Gets algorithm_status
    """

    def __init__(self, collection_name:str):
        ###############################################################################
        #                          Initiate database instance                         #
        ###############################################################################
        self._db = ApkManager.instance()
        self.c = self._db.get_collection(collection_name)


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


    def update_algorithm_status(self, uuid: str, update_dict: dict):
        # Get document ################################################################

        try:
            d = self._db.get_document(uuid, self.c)
            d = d[0]

            # p = {"status": status, "notes": notes, "estimate_remaining_time": estimate_remaining_time}

            for key, item in update_dict.items():
                if item == "" or item == None:
                    ###############################################################################
                    #                       Reuse old status object if empty                      #
                    ###############################################################################
                    item = d[key]

            status_key = 'algorithm_status'

            # Get status ##################################################################
            n = update_dict

            self._db.update_document(uuid, self.c, status_key, n)

        except Exception as e:
            print(e)
        else:
            return n


if __name__ == "__main__":
    pass
