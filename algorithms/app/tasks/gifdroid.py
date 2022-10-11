from tasks.enums.status_enum import StatusEnum
from resources.resource import *
from threading import Thread
from tasks.task import Task
from typing import List
import requests
import json, os

class Gifdroid(Task):
    """Class for managing gifdroid algorithm"""

    name = "Gifdroid"
    _output_types = [ResourceType.EXECUTION_TRACE]
    _input_types = [ResourceType.UTG, ResourceType.GIF]
    _execute_url = os.environ['GIFDROID']

    def __init__(self, output_dir: str, resource_dict: Dict[ResourceType, ResourceGroup], uuid: str) -> None:
        """
        Gifdroid manages a single gifdroid task. It subscribes to utg and gif resources. Whenever both a new utg and gif are added it starts running.

        TODO what if many gifs but with the same UTG? How to manage that?

        Parameters:
            output_dir - (str) The output directory for the gifdroid result
            resource_dict - (str) Dictionary of resource groups required by this algorithm # TODO try combine utg and gif into single resource group

        Returns: Nothing
        """
        super().__init__(output_dir, resource_dict, uuid)
        self._sub_to_utg()
        self._sub_to_gif()
        self.utg_path = None
        self.gif_path = None
        self.resource_dict = resource_dict


    def run(self) -> bool:
        """
        Execute gifdroid algorithm by http request and passing in necessary data for gifdroid to figure out stuff.
        """
        if self._check_resources_available():
            print(f'Running {self.name}.')

            data = {
                "gif_path": self.gif_path,
                "utg_path": self.utg_path,
                "output_dir": self.output_dir
            }

            self.update_algorithm_status(StatusEnum.running)
            response = requests.post(self._execute_url, data=json.dumps( data ), headers={'Content-Type': 'application/json'})

            if response.status_code == 200:
                self.update_algorithm_status(StatusEnum.successful)
            else:
                self.update_algorithm_status(StatusEnum.failed)

            return True

        return False


    def update_algorithm_status(self, status: StatusEnum):
        self.status = status.value

        data = {
            "status": self.status,
            "logs": f'{ self.name } is {self.status.lower()}.'
        }

        assert self.uuid != None, "No job UUID detected."
        algorithm_name = self.name[0].lower() + self.name[1:]
        url = os.path.join(self._status_controller, self.uuid, algorithm_name)
        res = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
        print(f'Updated {algorithm_name} status on url {url} to {self.status}. {res}.')


    def _check_resources_available(self):
        """
        Check if both gif and utg resource are both avalaible. TODO maybe combine both into one resource group?
        """
        if self.gif_path != None and self.utg_path != None:
            return True

        return False

    def utg_callback(self, utg : ResourceWrapper) -> None:
        """
        Callback method for using utg

        Parameters:
            utg - (ResourceWrapper) The resource that is need by gifdroid from droidbot. \
                Once both utf and gif are available, it will signal Gifdroid to run.
        """
        self.utg_path = utg.get_path()
        print('utg file ready for gifdroid')
        self.run()
        utg.release()


    def gif_callback(self, gif : ResourceWrapper) -> None:
        """
        Callback method for using gif

        Parameters:
            gif - (ResourceWrapper) The resource that is need by gifdroid from droidbot. \
                Once both utf and gif are available, it will signal Gifdroid to run.
        """
        self.gif_path = gif.get_path()
        print('gif file ready for gifdroid')
        self.run()
        gif.release()


    def _sub_to_utg(self) -> None:
        """Get notified when an emulator is available"""
        if ResourceType.UTG in self.resource_dict:
            self.resource_dict[ResourceType.UTG].subscribe(self.utg_callback)


    def _sub_to_gif(self) -> None:
        """Get notified when an emulator is available"""
        if ResourceType.GIF in self.resource_dict:
            self.resource_dict[ResourceType.GIF].subscribe(self.gif_callback)

    @classmethod
    def get_input_types(cls) -> List[ResourceType]:
        """Input resource types of the task"""
        return cls._input_types


    @classmethod
    def get_output_types(cls) -> List[ResourceType]:
        """Output resource types of the task"""
        return cls._output_types


    @classmethod
    def get_name(cls) -> str:
        """Name of the task"""
        return cls.name
