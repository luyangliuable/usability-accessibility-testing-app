from tasks.concurrency.file_watcher import FileWatcher
from tasks.enums.status_enum import StatusEnum
from resources.resource import *
from threading import Thread
from tasks.task import Task
from typing import List
from time import sleep
import typing as t
import requests
import logging
import os
import json


class Droidbot(Task, Thread):
    """Class for managing droidbot algorithm"""

    _input_types = [ResourceType.APK_FILE, ResourceType.EMULATOR]
    _output_types = [ResourceType.UTG, ResourceType.SCREENSHOT]
    _execute_url = os.environ['DROIDBOT']
    name = "Droidbot"

    def __init__(self, output_dir: str, resource_dict: Dict[ResourceType, ResourceGroup], uuid: str) -> None:
        """
        Droidbot class manages a single droidbot task. It subscribes to utg and gif resources. Whenever both a new utg and gif are added it starts running.


        Parameters:
            output_dir - (str) The output directory for the gifdroid result
            resource_dict - (str) Dictionary of resource groups required by this algorithm # TODO try combine utg and gif into single resource group

        Returns: Nothing
        """
        super().__init__(output_dir, resource_dict, uuid)
        self._sub_to_apks()
        self._sub_to_emulators()
        self.apk_queue = []
        self.images = ()
        self.check_new_image_directory = os.path.join(output_dir, 'states')
        self._image_file_watcher = FileWatcher(uuid, 'jpg', self.check_new_image_directory, ResourceType.SCREENSHOT, self)
        


    def _check_input_resources_available(self) -> bool:
        """
        Check if all resources are avalaible ( apk and emulator ).
        TODO maybe combine both into one resource group?

        Returns: (Boolean) Whether or not the resources are avalaible.
        """
        flag = True

        for resource in self._input_types:
            if not self.resource_dict[resource].is_active:
                flag = False
                break

        return flag


    def update_algorithm_status(self, status: StatusEnum):
        self.status = status

        data = {
            "status": self.status,
            "logs": f'{ self.name } is {self.status.value.lower()}.'
        }

        assert self.uuid != None, "No job UUID detected."
        algorithm_name = self.name[0].lower() + self.name[1:]
        url = os.path.join(self._status_controller, self.uuid, algorithm_name)
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
        print(f'Updated {algorithm_name} status on url {url} to {self.status}. {response}.')


    def _publish_utg(self) -> bool:
        utg = ResourceWrapper(self.output_dir, self.name)
        self.resource_dict[ResourceType.UTG].publish(utg, True)

        print(f'Published { utg } at {self.output_dir}.')
        return True


    # @staticmethod
    # def run(apk_path: str, output_dir: str) -> t.Dict[str, str]:
    #     """
    #     Execute gifdroid algorithm by http request and passing in necessary data for gifdroid to figure out stuff.

    #     Parameters:
    #         apk_path - (str) The string path for the apk for to run droidbot.


    #     # TODO make this a static method
    #     """
    #     self.update_algorithm_status(StatusEnum.running)
    #     self._image_file_watcher.start()
    #     response = requests.post(str( self._execute_url ), data=json.dumps(self._get_execution_data(apk_path)), headers={"Content-Type": "application/json"})


    #     if response.status_code == 200:
    #         self.update_algorithm_status(StatusEnum.successful)
    #     else:
    #         self.update_algorithm_status(StatusEnum.failed)

    #     self._image_file_watcher.join()
    #     self._publish_utg()

    #     return { "message": "Execute started." }


    def run(self, apk_path: str) -> t.Dict[str, str]:
        """
        Execute gifdroid algorithm by http request and passing in necessary data for gifdroid to figure out stuff.

        Parameters:
            apk_path - (str) The string path for the apk for to run droidbot.

        # TODO make this a staticmethod
        """
        self.update_algorithm_status(StatusEnum.running)
        self._image_file_watcher.start()
        print(self._execute_url)
        print(self._execute_url)
        print(self._execute_url)
        print(self._execute_url)
        response = requests.post(str( self._execute_url ), data=json.dumps(self._get_execution_data(apk_path)), headers={"Content-Type": "application/json"})


        if response.status_code == 200:
            self.update_algorithm_status(StatusEnum.successful)
        else:
            self.update_algorithm_status(StatusEnum.failed)

        self._image_file_watcher.join()
        self._publish_utg()

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
        print(data)

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
        while len(self.apk_queue) > 0:
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


