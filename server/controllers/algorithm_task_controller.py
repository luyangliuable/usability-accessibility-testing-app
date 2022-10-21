from controllers.algorithm_status_controller import *
from controllers.job_status_controller import *
from utility.enforce_bucket_existance import *
from controllers.controller import Controller
from enums.status_enum import StatusEnum
from enums.algorithm_enum import AlgorithmEnum
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

        self.collection_name = collection_name
        self.algorithm_status_controller = AlgorithmStatusController(collection_name)
        self.job_status_controller = JobStatusController(collection_name)
        self.shared_volume = '/home/data'


    def post(self, uuid: str, algorithms: t.List[AlgorithmEnum]) -> t.List[ AlgorithmEnum ]:
        """
        Post to signal start all the algorithms corresponding to a particular job by uuid.

        Parameters:
            uuid - job uuid
            algorithms_to_complete - List of algorithm info to finish.

        Returns: A list of task result information {"files": ["file_url_placeholder"], "images": ["image_url_placeholder"], "errors": str( errors ) }
        """

        # print(AlgorithmEnum['gifdroid'].value)

        # self.job_status_controller.post(uuid, start_time=start_time, status=StatusEnum.running.value, progress=10, logs="")
        self.acknowledge(uuid, algorithms)

        self._send_for_analysis(uuid, algorithms)

        return algorithms


    def _send_for_analysis(self, uuid: str, algorithms: t.List[AlgorithmEnum]) -> int:
        analysis_api = os.environ['ANALYSIS']

        data = {
            'algorithms': algorithms,
            'apk_file': self._get_apk_file(self.shared_volume, uuid),
            'additional_files': self._get_additional_files(self.shared_volume, uuid, algorithms),
            'uuid': uuid
        }

        print(f'Sending job for analysis with {data}.')

        requests.post(analysis_api, headers={"Content-Type": "application/json"}, json=data)


    def _get_additional_files(self, shared_volume: str, uuid: str, algorithms: t.List[AlgorithmEnum]) -> dict:
        additional_files = {}

        for alg in algorithms:

            additional_files[alg] = {}

        for algorithm in algorithms:
            additional_files_directory = os.path.join(shared_volume, uuid, algorithm)
            if os.path.exists(additional_files_directory):
                for file in os.listdir(additional_files_directory):
                    print(file)
                    file_type = file.split('.')[-1]

                    if file_type in additional_files:
                        additional_files[algorithm][file_type].append(os.path.join(additional_files_directory, file))
                    else:
                        additional_files[algorithm][file_type] = [os.path.join(additional_files_directory, file)]

        return additional_files

    def _get_apk_file(self, shared_volume: str, uuid: str) -> str:
        apk_directory = os.path.join(shared_volume, uuid)
        apk_file_suffix = "apk"

        for file in os.listdir(apk_directory):
            if file[len(file)-3: len(file)] == apk_file_suffix:
                return os.path.join( apk_directory, file )

        raise FileNotFoundError("No apk file")


    def acknowledge(self, uuid: str, algorithms_to_run: t.List[str]) -> bool:
        """
        Acknowledge the job start by updating the metadata on mongodb such as its status, start_time and progress.

        Parameters:
            uuid - job uuid
            algorithms - the list of algorithms to run

        Returns: (bool) if the algorithm transaction is successful.
        """
        job_start_log = "Job started"
        current_time = dt.now()
        self.job_status_controller.post(
            uuid,
            status=StatusEnum.running.value,
            start_time=current_time,
            log=job_start_log,
            algorithms_to_run=algorithms_to_run
        )
        return True

    def get(self, uuid: str):
        pass


    def insert(self, uuid: str, **kwargs):
        pass
