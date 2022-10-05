# from tasks.xbot import Xbot
# from tasks.tappability import Tappability
from tasks.droidbot import Droidbot
# from tasks.owleye import Owleye
from tasks.gifdroid import Gifdroid
from resources.screenshot import Screenshot
from tasks.task import *
from resources.resource import *
from resources.resource_types import ResourceType
from typing import Dict, List
import os
import uuid


class ApkAnalysis:
    """This class runs all algorithms and generates the combined results"""

    def __init__(self, output_dir, names, apk_file: str, additional_files: Dict[str, Dict[str, str]]={}) -> None:
        self.required_resources = [ResourceType.EMULATOR, ResourceType.APK_FILE]
        self.pending_published = {} # Temporary but needed variable until a better way
        self.apk = ResourceWrapper(apk_file, 'upload')
        emulator_link = 'host.docker.internal:5555'
        self.additional_files = additional_files
        self.emulator = ResourceWrapper('', emulator_link)
        self.output_dir = output_dir
        self.apk_file = apk_file
        self.resources = {}
        self._init_dirs()
        self.name = names
        self._init_dirs()

        print(f'APK file is {apk_file}')



    def get_emulator(self) -> ResourceWrapper:
        return self.emulator


    def get_apk(self) -> ResourceWrapper:
        return self.apk


    def start_processing(self) -> None:
        """Creates required tasks and starts them"""
        self._init_resource_groups()
        self._init_additional_resource_groups()

        print(f'Creating tasks {self.name} with output dir {self.output_dir} and res {self.resources}')
        TaskFactory.create_tasks(self.name, self.output_dir, self.resources)

        self._publish_apk()
        self._publish_emulator()
        self._publish_additional_files()


    def _publish_additional_files(self):
        """
        Re-publish all files because algorithm won't run unless trigger publish again.
        """
        for algorithm, additional_files in self.additional_files.items():
            for resource_type_name, files in additional_files.items():
                file = files[0] # Assume each algorithm has 1 additional file
                resource_type = ResourceType[resource_type_name.upper()]
                resource_wrapper = ResourceWrapper(file, 'initialization')
                self.resources[resource_type].publish(resource_wrapper, True)
                print(f'Published resource type {resource_type} for {algorithm} with {file}.')


    def _publish_apk(self):
        self.resources[ResourceType.APK_FILE].publish(self.apk, True)


    def _publish_emulator(self):
        self.resources[ResourceType.EMULATOR].publish(self.emulator, True)


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
        for resource in self.required_resources:
            self.resources[resource] = ResourceGroup(resource)

        print(self.required_resources)


    def _init_additional_resource_groups(self) -> None:
        for algorithm, additional_files in self.additional_files.items():
            for resource_type_name, _ in additional_files.items():
                resource_type = ResourceType[resource_type_name.upper()]
                self.resources[resource_type] = ResourceGroup(resource_type)
                print(f'Initialised resource type {resource_type} for {algorithm}.')



if __name__ == '__main__':
    # lst = [Screenshot]
    resource_dict = {} # make resource dict
    resources = [ResourceType.APK_FILE, ResourceType.EMULATOR]
    # names = ['Xbot', 'Tappability']
    names = ['Droidbot']
    AA = ApkAnalysis("random_uuid", "/Users/blackfish/Documents/FIT3170_Usability_Accessibility_Testing_App/algorithms/app/.data/", names, resources)
    AA.start_processing()
