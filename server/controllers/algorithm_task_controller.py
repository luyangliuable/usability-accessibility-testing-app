from controllers.algorithm_status_controller import *
from controllers.job_status_controller import *
from utility.enforce_bucket_existance import *
from controllers.controller import Controller
from enums.status_enum import StatusEnum
from utility.uuid_generator import *
from datetime import datetime as dt
from models.DBManager import *
from tasks import worker
from celery import Task
import typing as t
import requests
import json


T = t.TypeVar('T')


class AlgorithmTaskController(t.Generic[T], Controller, Task):

    bucket_name = 'apk-bucket'

    def __init__(self, collection_name: str) -> None:
        """
        This controller is responsible for download file stored from previous job into the s3 bucket.

        Parameters:
            collection_name - The collection name to refer to for database.
            json_result_file_parser - A strategy for parsing result files into a json to update file names mongodb schema.

        """

        self.cn = collection_name
        self.asc = AlgorithmStatusController(collection_name)
        self.jsc = JobStatusController(collection_name)


    def post(self, uuid: str, algorithms_to_complete: t.List[t.Dict[str, str]]) -> t.List[ t.Dict ]:
        """
        Post to signal start all the algorithms corresponding to a particular job by uuid.

        Parameters:
            uuid - job uuid
            algorithms_to_complete - List of algorithm info to finish.

        Returns: A list of task result information {"files": ["file_url_placeholder"], "images": ["image_url_placeholder"], "errors": str( errors ) }
        """

        tasks = [{} for _ in range(len(algorithms_to_complete))]

        self.jsc.post(uuid, start_time=str( dt.now() ), status=StatusEnum.running.value, progress=10, logs="Job started")

        for i, alg in enumerate( algorithms_to_complete ):
            task_info = {"uuid": uuid, "algorithm": alg['uuid']}
            # tasks[i] = run_algorithm.delay(task_info)
            # tasks[i] = worker.register_task(self._execute_algorithm.delay(task_info))
            tasks[i] = self._execute_algorithm(task_info)
            self.acknowledge(uuid, alg['uuid'])

        return tasks

    # @worker.task(name="run_algorithm")
    def _execute_algorithm(self, info: t.Dict) -> t.Dict:
        errors = []

        start_links = {
            "storydistiller": os.environ.get("STORYDISTILLER"),
            "xbot": os.environ.get("XBOT"),
            "owleye": os.environ.get("OWLEYE"),
            "gifdroid": os.environ['GIFDROID'],
            "droidbot": os.environ['DROIDBOT'],
            "tappable": "SKIP"
        }


        uuid = info["uuid"]
        algorithm = info['algorithm']
        URL = start_links[algorithm]

        print(f'TASK: Running { algorithm } url: { URL }')
        print(f'TASK: Algorithm cluster uuid is { uuid }')

        self._mark_algorithm_started(uuid, algorithm)

        ###############################################################################
        #                          Signal Algorithm to start                          #
        ###############################################################################
        result = self._signal_start(uuid, URL)

        ###############################################################################
        #           Update status according to the success of the algorithm           #
        ###############################################################################
        if result.status_code < 400:
            self._mark_algorithm_successful(uuid, algorithm)
            print("TASK: Successfully completed task", algorithm)
        else:
            self._mark_algorithm_failed(uuid, algorithm)
            print("TASK: FAILED complete task", algorithm)

        return {"files": ["file_url_placeholder"], "images": ["image_url_placeholder"], "errors": str( errors ) }


    def acknowledge(self, uuid: str, algorithm: str) -> bool:
        """
        Acknowledge the tasks for each algorithm by updating the metadata on mongo database such as its status, start_time and progress.

        Parameters:
            uuid - job uuid
            algorithm - the algorithm to acknowldge

        Returns: (bool) if the algorithm transaction is successful.
        """
        self.asc.post(uuid, algorithm, status=StatusEnum.running.value, start_time=str( dt.now() ), progress=10)
        return True

    def _mark_algorithm_started(self, uuid: str, algorithm: str):
        flask_backend = os.environ['FLASK_BACKEND']
        update_status_url = os.path.join(flask_backend, 'status', 'update', uuid, algorithm)

        requests.post(update_status_url, headers={"Content-Type": "text/plain"}, data=StatusEnum.running.value )


    def _mark_algorithm_failed(self, uuid: str, algorithm: str):
        flask_backend = os.environ['FLASK_BACKEND']
        update_status_url = os.path.join(flask_backend, 'status', 'update', uuid, algorithm)

        requests.post(update_status_url, headers={"Content-Type": "text/plain"}, data=StatusEnum.failed.value )


    def _mark_algorithm_successful(self, uuid: str, algorithm: str):
        flask_backend = os.environ['FLASK_BACKEND']
        update_status_url = os.path.join(flask_backend, 'status', 'update', uuid, algorithm)

        requests.post(update_status_url, headers={"Content-Type": "text/plain"}, data=StatusEnum.successful.value )


    def _signal_start(self, uuid: str,  algorithm_api_endpoint: str):
        apk_file = "a2dp.Vol_133.apk"
        execution_data = {
            "uuid": uuid,
            "apk_path": os.path.join("/home/data", uuid, apk_file),
            "output_dir": "/home/data/droidbot/"
        }

        print(execution_data['apk_path'])
        print(execution_data['apk_path'])
        print(execution_data['apk_path'])
        print(execution_data['apk_path'])
        print(execution_data['apk_path'])
        print(execution_data['apk_path'])
        print(execution_data['apk_path'])
        print(execution_data['apk_path'])
        print(execution_data['apk_path'])
        print(execution_data['apk_path'])
        print(execution_data['apk_path'])
        print(execution_data['apk_path'])

        result = requests.post("http://host.docker.internal:3008/new_job", data=json.dumps(execution_data), headers={"Content-Type": "application/json"})
        return result


    def get(self, uuid: str):
        pass


    def insert(self, uuid: str, **kwargs):
        pass
