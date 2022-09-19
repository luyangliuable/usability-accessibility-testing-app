from tasks.task import *
from resources.resource import *
from typing import List
import os


class ApkAnalysis:
    """This class runs all algorithms and generates the combined results"""
    
    def __init__(self, output_dir, req_results:List[ResourceType], apk_file=None) -> None:
        self.output_dir = output_dir
        self. req_results = req_results
        self.tmp_dir = os.path.join(output_dir, "temp")
        self._init_dirs()
        self.apk_resources = {}
        self.tasks = []
        self.apk_file = apk_file

    def start_processing(self) -> None:
        """Creates required tasks and starts them"""
        # TODO create task classes
        pass
    
    def get_results(self) -> None:
        """Generates results in output dir"""
        # TODO create task class for getting results
        pass
    
    def _init_dirs(self) -> None:
        """Creates directories for analysis"""
        # create output dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        # create temp dir
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)
    
    def _init_resource_groups(self) -> None:
        # TODO create resource groups
        pass
            