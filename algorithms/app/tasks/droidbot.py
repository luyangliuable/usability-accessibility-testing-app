from tasks.task import Task
from resources.resource import *
from typing import List
import typing as t
import os
import json
import requests

class Droidbot(Task):
    """Class for managing droidbot algorithm"""

    _input_types = [ResourceType.APK_FILE, ResourceType.EMULATOR]
    _output_types = [ResourceType.JSON_LAYOUT, ResourceType.UTG]
    _execute_url = "http://localhost:3008/new_job"
    name = "Droidbot"
    _shared_volume = "/home/tasks"


    def __init__(self, output_dir: str, resource_dict: Dict[ResourceType, ResourceGroup], execution_data: Dict[str, str]) -> None:
        """
        Droidbot class manages a single droidbot task. It subscribes to utg and gif resources. Whenever both a new utg and gif are added it starts running.


        Parameters:
            output_dir - (str) The output directory for the gifdroid result
            resource_dict - (str) Dictionary of resource groups required by this algorithm # TODO try combine utg and gif into single resource group

        Returns: Nothing
        """
        super().__init__(output_dir, resource_dict, execution_data)
        self.emulator = resource_dict[ResourceType.EMULATOR]
        self._sub_to_apks()
        self._sub_to_emulators()
        self.apk_queue = []


    def run(self, apk_path: str) -> t.Dict[str, str]:
        """
        Execute gifdroid algorithm by http request and passing in necessary data for gifdroid to figure out stuff.

        Parameters:
            apk_path - (str) The string path for the apk for to run droibot.
        """
        print(json.dumps(self._get_execution_data(apk_path)))
        requests.post(str( self._execute_url ), data=json.dumps(self._get_execution_data(apk_path)), headers={"Content-Type": "application/json"})

        return { "message": "Execute started." }


    def _get_execution_data(self, apk_path: str):

        """
        Get the execution data necessary to execute droidbot

        Parameters:
            apk_path - (str) The string path for the apk for to run droibot.
        """
        data = {
            "apk_path": apk_path,
            "output_dir": self.output_dir,
        }

        return data


    def _sub_to_apks(self) -> None:
        """Get notified when a new APK is available"""
        if ResourceType.APK_FILE in self.resource_dict:
            self.resource_dict[ResourceType.APK_FILE].subscribe(self.apk_callback) # calls add_apk() when new apk is available


    def apk_callback(self, new_apk : ResourceWrapper) -> None:
        """callback method to add apk and run algorithm"""
        if new_apk not in self.apk_queue:
            self.apk_queue.append(new_apk)


    def emulator_callback(self, emulator : ResourceWrapper) -> None:
        """callback method for using emulator"""
        self._process_apks()
        emulator.release()


    def _process_apks(self) -> None:
        while len(self.apk_queue) > 0:                                      # get next apk
            apk = self.apk_queue.pop(0)
            apk_path = apk.get_path()
            self.run(apk_path)
            apk.release()


    def _sub_to_emulators(self) -> None:
        """Get notified when an emulator is available"""
        if ResourceType.EMULATOR in self.resource_dict:
            self.resource_dict[ResourceType.EMULATOR].subscribe(self.emulator_callback)


    @classmethod
    def get_name(cls) -> str:
        """Name of the task"""
        return cls.name


    @classmethod
    def get_input_types(cls) -> List[ResourceType]:
        """Input resource types of the task"""
        return cls._input_types


    @classmethod
    def get_output_types(cls) -> List[ResourceType]:
        """Output resource types of the task"""
        return cls._output_types
