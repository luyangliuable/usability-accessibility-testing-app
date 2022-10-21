import os
# from numpy import result_type
from utility.uuid_generator import unique_id_generator
from typing import TypeVar, Generic, List, Dict, Tuple
from controllers.controller import Controller
from enums.status_enum import StatusEnum
from models.DBManager import DBManager


T = TypeVar('T')


class AlgorithmDataController(Generic[T], Controller):
    """
    This controller class is used to update metadata for files on mongodb for traceability purpose.
    """

    results_key = "results"

    def __init__(self, collection_name: str) -> None:
        """
        This controller class is used to update metadata for files on mongodb for traceability purpose.

        Parameters:
            collection_name - (str) name of collection on *mongodb* which is apk.
            json_result_file_parser - (Strategy) will not be used but still not updated because backend not finished

        Returns: None
        """
        self.collection_name = collection_name
        self._db = DBManager.instance()
        self.collection = self._db.get_collection('apk')

        self.lookup = {
            "owleye": "activities",
            "storydisitiller": "activities",
            "xbot": "activities",
            "gifdroid": "gifdroid",
            "droidbot": "gifdroid",
        }

    def get(self, uuid: str):
        """
        Get file metadata that matches the job uuid

        Parameters:
            uuid (str) - The job uuid the identifies the cluster of algorithms to run
        """

        return self._db.get_document(uuid=uuid, collection=self.collection)


    def post(self, uuid: str, algorithm: str, new_data: T) -> bool:
        """
        Add file metadata that matches the job uuid


        Parameters:
            request_parameters - request parameters that contain contents of document
        """

        # self.collection.update_one({"uuid": uuid}, {'$push': {f'results.ui-states.{ algorithm }': new_data}})

        # result = self._db.get_document(uuid, self.collection)[self.results_key]['ui-states'][algorithm]

        # return result


        self._insert_algorithm_result(uuid, algorithm, new_data)
        return new_data


    def _insert_utg_result(self, uuid: str, data: Dict) -> Dict[str, T]:
        results_schema = self._db.get_document(uuid, self.collection)[self.results_key]

        results_schema['utg'] = data;

        self._db.update_document(uuid, self.collection, self.results_key, results_schema)

        return results_schema;


    def _insert_algorithm_result(self, uuid: str, algorithm: str, data: dict) -> dict:
        """
        This function inserts the links to the algorithm results into the document matching uuid

        Parameters:
            uuid - uuid for the job which is the cluster of algorithms tasked to run
            algorithm - the algorithm the result links for
            links_to_res - the single link to result. NOTE that element in list is dynamically typed so it can be a string

        Returns: Dictionary for the updated document and a bool if the method is successful.

        """
        algorithm = algorithm.lower()
        alg_results = self._db.get_document(uuid, self.collection)[self.results_key]

        ui_state_results = ['xbot', 'owleye', 'tappable']
        if algorithm in ui_state_results:
            alg_results['ui-states'][algorithm].append(data)

        new_gifdroid = alg_results['gifdroid']
        if algorithm ==  'gifdroid':
            for name, data in data.items():
                new_gifdroid[name] = data
            alg_results['gifdroid'] = new_gifdroid


        self._db.update_document(uuid, self.collection, self.results_key, alg_results)

        print(alg_results['ui-states'])
        return alg_results


    def _get_utg(self, uuid: str) -> Dict[str, T]:
        """
        Method for getting a document from api

        Parameters:
            uuid - the unique id for the job containing algorithm run.
            algorithm - the algorithm

        Returns: The result slice in the schema for the algorithm

        """

        document = self.get(uuid)
        result = document[self.results_key]['utg']

        return result


    def _get_result_of_algorithm(self, uuid: str, type: str) -> Dict[str, T]:
        """
        Method for getting a document from api

        Parameters:
            uuid - the unique id for the job containing algorithm run.
            algorithm - the algorithm

        Returns: The result slice in the schema for the algorithm

        TODO: fix this method to return the correct result
              Currently it returns the entire document and not just the results for the algorithm
        """

        schema_result_key = 'results'
        document = self.get(uuid)
        result = document[schema_result_key][type]

        return result

    def _get_lookup(self) -> Dict[str, str]:
        return self.lookup
