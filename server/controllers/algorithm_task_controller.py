from controllers.algorithm_status_controller import *
from utility.enforce_bucket_existance import *
from enums.status_enum import StatusEnum
from tasks import run_algorithm, celery
from utility.uuid_generator import *
from models.DBManager import *
import typing as t


T = t.TypeVar('T')


class AlgorithmTaskController(t.Generic[T]):

    bucket_name = 'apk-bucket'

    def __init__(self, collection_name: str) -> None:
        """
        This controller is responsible for download file stored from previous job into the s3 bucket.

        Parameters:
            collection_name - The collection name to refer to for database.
            json_result_file_parser - A strategy for parsing result files into a json to update file names mongodb schema.

        """

        self.cn = collection_name
        # self._db = DBManager.instance()
        self.asc = AlgorithmStatusController(collection_name)


    def post(self, uuid: str, algorithms_to_complete: t.List[t.Dict[str, str]]) -> t.List[ t.Dict ]:

        tasks = [{} for _ in range(len(algorithms_to_complete))]

        for i, alg in enumerate( algorithms_to_complete ):
            print(alg)
            task_info = {"uuid": uuid, "algorithm": alg['uuid']}
            print(task_info)
            tasks[i] = run_algorithm.delay(task_info)
            self.acknowledge(uuid, alg['uuid'])

        return tasks


    def acknowledge(self, uuid: str, algorithm: str) -> bool:
        self.asc.update(uuid, algorithm, status=str( StatusEnum.running ))
        return True

