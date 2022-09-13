from tasks.task import Task
from resources import *
from typing import List
import os

class Storydistiller(Task):
    """Class for managing Storydistiller algorithm"""
    
    _input_types = [ResourceType.APK_FILE, ResourceType.EMULATOR]
    _output_types = [ResourceType.SCREENSHOT_PNG, ResourceType.XML_LAYOUT]
    
    def __init__(self, output_dir) -> None:
        super().__init__(output_dir)
        self.apk_path = apk_path

    @classmethod
    def get_name() -> str:
        """Name of the task"""
        return Storydistiller.__name__
    
    @classmethod
    def get_input_types() -> List[ResourceType]:
        """Input resource types of the task"""
        return Storydistiller._input_types

    @classmethod
    def get_output_types() -> List[ResourceType]:
        """Output resource types of the task"""
        return Storydistiller._output_types
    
    def execute(self) -> None:
        data = {
            "apk_path":self.apk_path,
            "output_dir":self.output_dir,
            "emulator": self.emulator
        }
        response = self.http_request(url=self.url, data=data)
        
        self.status = 'SUCCESSFUL' if response and response.status_code==200 else 'FAILED'

    def run_storydisiller(self) -> None:
        pass