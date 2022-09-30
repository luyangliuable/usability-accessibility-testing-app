from tasks.xbot import Xbot
from tasks.tappability import Tappability
from tasks.droidbot import Droidbot
from tasks.owleye import Owleye
from tasks.gifdroid import Gifdroid
from resources.screenshot import Screenshot
from tasks.task import *
from resources.resource import *
from resources.resource_types import ResourceType
from typing import List
import os
import uuid


class ApkAnalysis:
    """This class runs all algorithms and generates the combined results"""
    
    def __init__(self, output_dir, names, req_results:List[ResourceType], apk_file=None) -> None:
        self.output_dir = output_dir
        self. req_results = req_results
        self._init_dirs()
        self.apk_resources = {}
        self.name = names
        self.apk_file = apk_file

    def start_processing(self) -> None:
        """Creates required tasks and starts them"""
        self._init_resource_groups()

        execution_data = {
            "apk_path": "/home/data/test_apks/a2dp.Vol_133/a2dp.Vol_133.apk",
        }

        start = TaskFactory.create_tasks(self.uuid, self.name, self.output_dir, self.apk_resources, execution_data)
        # start = [task.execute() for task in start]
    
    def get_results(self) -> None:
        """Generates results in output dir"""
        # TODO create task class for getting results
        pass
    
    def _init_dirs(self) -> None:
        """Creates directories for analysis"""
        # create output dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def _init_apk_resource(self) -> ResourceGroup:
        rw = ResourceWrapper(self.apk_file, None)
        rg = ResourceGroup(ResourceType.APK_FILE).publish(rw, True)
        return rg
    
    def _init_resource_groups(self) -> None:
        # TODO create resource groups 
        for resource in self.req_results:
            self.apk_resources[resource]= ResourceGroup(resource)
        self.apk_resources[ResourceType.APK_FILE] = self._init_apk_resource()
        
if __name__ == '__main__':
    # lst = [Screenshot]
    resource_dict = {} # make resource dict
    resources = [ResourceType.APK_FILE, ResourceType.EMULATOR]
    # names = ['Xbot', 'Tappability']
    names = ['Droidbot']
    AA = ApkAnalysis("random_uuid", "/Users/blackfish/Documents/FIT3170_Usability_Accessibility_Testing_App/algorithms/app/.data/", names, resources)
    AA.start_processing()
