from controllers.algorithm_status_controller import *
from controllers.job_status_controller import *
from utility.enforce_bucket_existance import *
from enums.status_enum import StatusEnum
from tasks import run_algorithm, celery
from controllers.controller import Controller
from utility.uuid_generator import *
from models.DBManager import *
from datetime import datetime as dt
import typing as t


T = t.TypeVar('T')


class AlgorithmTaskController(t.Generic[T], Controller):

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

        self.jsc.update(uuid, start_time=str( dt.now() ), status=StatusEnum.running.value, progress=10, logs="Job started")

        for i, alg in enumerate( algorithms_to_complete ):
            task_info = {"uuid": uuid, "algorithm": alg['uuid']}
            tasks[i] = run_algorithm.delay(task_info)
            self.acknowledge(uuid, alg['uuid'])

        return tasks


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


    def get(self, uuid: str):
        pass


    def insert(self, uuid: str, **kwargs):
        pass
