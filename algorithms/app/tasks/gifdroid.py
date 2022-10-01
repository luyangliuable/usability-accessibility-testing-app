from tasks.task import Task
from resources.resource import *
from typing import List
import requests
import json, os

class Gifdroid(Task):
    """Class for managing gifdroid algorithm"""

    name = "Gifdroid"
    _input_types = [ResourceType.APK_FILE, ResourceType.EMULATOR]
    _output_types = [ResourceType.JSON_LAYOUT, ResourceType.UTG]
    _execute_url = "http://localhost:3005/new_job"

    def __init__(self, output_dir: str, resource_dict: Dict[ResourceType, ResourceGroup]) -> None:
        """
        Gifdroid manages a single gifdroid task. It subscribes to utg and gif resources. Whenever both a new utg and gif are added it starts running.

        TODO what if many gifs but with the same UTG? How to manage that?

        Parameters:
            output_dir - (str) The output directory for the gifdroid result
            resource_dict - (str) Dictionary of resource groups required by this algorithm # TODO try combine utg and gif into single resource group

        Returns: Nothing
        """
        super().__init__(output_dir, resource_dict)
        self._sub_to_utg()
        self._sub_to_gif()
        self.utg_path = None
        self.gif_path = None

    def run(self) -> bool:
        """
        Execute gifdroid algorithm by http request and passing in necessary data for gifdroid to figure out stuff.
        """
        if self._check_resources_available():
            data = {
                "gif_path": self.gif_path,
                "utg_path": self.utg_path,
                "output_dir": self.output_dir
            }

            requests.post(self._execute_url, data=json.dumps( data ), headers={'Content-Type': 'application/json'})

            return True

        return False


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
        print(self.utg_path)
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
        print(self.gif_path)
        print(self.gif_path)
        print(self.gif_path)
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
