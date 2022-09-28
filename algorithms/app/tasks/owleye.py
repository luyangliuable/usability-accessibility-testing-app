from tasks.task import Task
from resources.resource import *
from typing import List
import os

class Owleye(Task):
    """Class for managing Owleye algorithm"""
    
    def __init__(self, image_dir, output_dir) -> None:
        super().__init__(output_dir, "owleye")
        self.image_dir = image_dir

    def execute(self) -> None:  
        data = {
            "image_dir":self.image_dir,
            "output_dir":self.output_dir
        }
        response = self.http_request(url=self.url, data=data)
        
        self.status = 'SUCCESSFUL' if response and response.status_code==200 else 'FAILED'
        
def get_display_issues(self) -> str:
        # run xbot and droidbot if not already run
        self._run_image_algorithms()
        # copy screenshots into temp folder convert PNGs to JPEG
        img_path = os.path.join(TEMP_PATH, "owleye", "screenshots")
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        self._move_files_xb(img_path, jpg = True)
        self._move_files_db(img_path)
        # run owleye
        owleye = Owleye(img_path, os.path.join(TEMP_PATH, "owleye")) #check inputs
        self.execute_task(owleye)
        # copy results into activity folders
        self._get_ui_display_issues(owleye=True) #separates results by activity
        return None

def _get_ui_display_issues(self, tappability = False, owleye = False, xbot=False):
        """Separates display issues by activity per algorithm"""
        activites_path = os.path.join(self.output_dir, "activities")
        for activity_name in list(set(self.activity_list)):
            tap_temp_path = os.path.join(TEMP_PATH, "tappability", activity_name)
            if tappability and os.path.exists(tap_temp_path):
                tap_path = os.path.join(activites_path, activity_name, "tappability_prediction")
                if not os.path.exists(tap_path):
                    os.makedirs(tap_path)
                for file in os.listdir(tap_temp_path):
                    shutil.copy(os.path.join(tap_temp_path, file), os.path.join(activites_path, activity_name, "tappability_prediction"))
            if owleye and os.path.exists(os.path.join(TEMP_PATH, "owleye", activity_name + '.jpg')):
                if not os.path.exists(os.path.join(activites_path, activity_name, "display_issues")):
                    os.makedirs(os.path.join(activites_path, activity_name, "display_issues"))
                shutil.copy(os.path.join(TEMP_PATH, "owleye", activity_name + '.jpg'), os.path.join(activites_path, activity_name,"display_issues"))
            return None