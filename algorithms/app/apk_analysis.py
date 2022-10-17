from resources.resource import *
from resources.resource_types import ResourceType
from models.emulator import Emulator
from models.screenshot import Screenshot
from typing import Dict, List
import os
from tasks.task import *
from tasks.xbot import *
from tasks.owleye import *
from tasks.tappability import Tappability
from tasks.droidbot import *
from tasks.gifdroid import *

EMULATOR = Emulator("emulator-5558", "host.docker.internal:5559", (1920, 1080))

class ApkAnalysis:
    """This class runs all algorithms and generates the combined results"""

    def __init__(self, output_dir: str, apk_path: str, req_tasks: list[str], additional_files: Dict[str, Dict[str, str]]={}) -> None:
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.apk_resource = ResourceWrapper(apk_path, 'upload')
        self.upload_additional_files = additional_files
        self.req_tasks = req_tasks
        self.resources = {}
        self._init_resource_groups()
        print(f'New APK Analysis.\nAPK file is {apk_path}')


    def start_processing(self, uuid=None) -> None:
        """Creates required tasks and starts them"""
        self._create_tasks(uuid)
        # publish provided files to start processing
        self._publish_provided_files()

    def _init_resource_groups(self) -> None:
        # create apk, screenshot and emulator resources for every instance
        self.resources[ResourceType.APK_FILE] = ResourceGroup(ResourceType.APK_FILE)
        self.resources[ResourceType.SCREENSHOT] = ResourceGroup(ResourceType.SCREENSHOT)
        self.resources[ResourceType.UTG] = ResourceGroup(ResourceType.UTG)
        self.resources[ResourceType.EMULATOR] = ResourceGroup(ResourceType.EMULATOR, usage=ResourceUsage.SEQUENTIAL) #TODO: implement singleton for emulator

        for name in self.req_tasks:
            for resource_type in TaskFactory._tasks[name].get_output_types():
                if resource_type not in self.resources:
                    self.resources[resource_type] = ResourceGroup(resource_type)

        # create optional resources
        for algorithm, algorithm_additional_files in self.upload_additional_files.items():
            for resource_type_name, _ in algorithm_additional_files.items():
                resource_type = ResourceType[resource_type_name.upper()]
                if resource_type not in self.resources:
                    self.resources[resource_type] = ResourceGroup(resource_type)
                print(f'Initialised resource type {resource_type} for {algorithm}.')
        print(f"Initialised resource groups: {self.resources.keys()}")

    def _create_tasks(self, uuid) -> None:
        # create tasks
        print(f'Creating tasks {self.req_tasks} with output dir {self.output_dir} and res {self.resources}')
        TaskFactory.create_tasks(self.req_tasks, self.output_dir, self.resources, uuid)

    def _publish_provided_files(self):
        # publish apk
        self.resources[ResourceType.APK_FILE].publish(self.apk_resource, True)
        # publish emulator
        self.resources[ResourceType.EMULATOR].publish(ResourceWrapper('', '', EMULATOR), True) #TODO: move this to singleton
        # publish additional_files
        print(self.upload_additional_files)
        for algorithm in self.upload_additional_files.keys():
            for resource_type_name, files in self.upload_additional_files[algorithm].items():
                resource_type = ResourceType[resource_type_name.upper()]
                file = files[0] # Assume is the first file.
                rw = ResourceWrapper(file, 'upload')
                self.resources[resource_type].publish(rw, True)

    def _publish_additional_files(self):
        """
        Re-publish all files because algorithm won't run unless trigger publish again.
        """
        for algorithm, algorithm_additional_files in self.upload_additional_files.items():
            for resource_type_name, files in algorithm_additional_files.items():
                file = files[0] # Assume each algorithm has 1 additional file
                resource_type = ResourceType[resource_type_name.upper()]
                resource_wrapper = ResourceWrapper(file, 'initialization')
                self.resources[resource_type].publish(resource_wrapper, True)
                print(f'Published resource type {resource_type} for {algorithm} with {file}.')

if __name__ == '__main__':
    a = ApkAnalysis('/home/data/test/a2dp.Vol_133/', '/home/data/test/a2dp.Vol_133/a2dp.Vol_133.apk', ["Xbot", "Owleye"])
    a.start_processing()
