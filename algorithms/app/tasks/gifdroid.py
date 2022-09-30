from tasks.task import Task
from resources.resource import *
from typing import List
import requests
import os

class Gifdroid(Task):
    """Class for managing gifdroid algorithm"""

    _input_types = [ResourceType.APK_FILE, ResourceType.EMULATOR]
    _output_types = [ResourceType.JSON_LAYOUT, ResourceType.UTG]
    name = "Gifdroid"

    def __init__(self, uuid,  apk_path, output_dir, execution_data) -> None:
        self.gif_path = execution_data['gif_path']
        self.apk_path = apk_path
        self.utg_path = execution_data['droidbot_result_dir']
        super().__init__(uuid, output_dir, "gifdroid", None, execution_data)

    def run(self) -> None:
        data = {
            "gif_path": self.gif_path,
            "apk_path": self.apk_path,
            "output_dir": self.output_dir
        }

        URL = "http://host.docker.internal:3005/new_job"
        uuid = "ransdasd"

        result = requests.post(str( URL ), json={ "uid": uuid })


    @classmethod
    def get_input_types(cls) -> List[ResourceType]:
        """Input resource types of the task"""
        return cls._input_types


    @classmethod
    def get_output_types(cls) -> List[ResourceType]:
        """Output resource types of the task"""
        return cls._output_types


    def get_execution_trace(self) -> str:
        # run droidbot
        self._run_image_algorithms(xbot=False)
        # copy utg into gifdroid input folder
        img_path = os.path.join(TEMP_PATH,"gifdroid")
        # run gifdroid
        gifdroid = Gifdroid() #check path
        self.execute_task(gifdroid)
        return None


    @classmethod
    def get_name(cls) -> str:
        """Name of the task"""
        return cls.name

    def _sub_to_apks(self) -> None:
        """Get notified when a new APK is available"""
        if ResourceType.APK_FILE in self.resource_dict:
            self.resource_dict[ResourceType.APK_FILE].subscribe(self.apk_callback) # calls add_apk() when new apk is available
