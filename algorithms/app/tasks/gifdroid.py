from tasks.task import Task
from resources.resource import *
from typing import List
import os

class Gifdroid(Task):
    """Class for managing gifdroid algorithm"""
    
    def __init__(self, gif_path, utg_path, output_dir) -> None:
        self.gif_path = gif_path
        self.utg_path = utg_path
        super().__init__(output_dir, "gifdroid", None)

    def execute(self) -> None:
        # TODO: implement method
        pass
    
      
    def get_execution_trace(self) -> str:
        # run droidbot
        self._run_image_algorithms(xbot=False)
        # copy utg into gifdroid input folder
        img_path = os.path.join(TEMP_PATH,"gifdroid")
        # run gifdroid
        gifdroid = Gifdroid() #check path
        self.execute_task(gifdroid)
        return None
   