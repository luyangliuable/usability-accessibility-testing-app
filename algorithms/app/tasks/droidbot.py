from tasks.task import Task
from resources.resource import *
from typing import List
import os
import json

class Droidbot(Task):
    """Class for managing droidbot algorithm"""
    
    def __init__(self, apk_path, output_dir, emulator) -> None:
        self.apk_path = apk_path
        self.emulator = emulator
        super().__init__(output_dir, "droidbot", None)

    def execute(self) -> None:
        # TODO: implement method
        pass
    
    def _move_files_db(self,img_dest, json_dest=None, activity=False):
        """Moves droidbot image and json files from task folder to temp directory. Renames files by activity name."""
        src = os.path.join(TEMP_PATH,"droidbot" ,"states")
        activites_path = os.path.join(self.output_dir, "activities")
        for file in os.listdir(src):
            if file.endswith(".json"):
                file_name = file.strip("state").strip("json")
                with open(os.path.join(src, file), 'r') as json_file:
                    json_out = json.loads(json_file.read())
                    activity_name = json_out["activity_stack"][0].replace("/", "_") #replace / with _ to not create folders instead of path names
                    if activity:
                        if not os.path.exists(os.path.join(activites_path, activity_name)):
                            os.makedirs(os.path.join(activites_path, activity_name))
                            os.makedirs(os.path.join(activites_path, activity_name, "screenshots"))
                            os.makedirs(os.path.join(activites_path, activity_name, "annotations"))
                        json_dest = os.path.join(self.output_dir, "activities", activity_name, "annotations")
                        img_dest = os.path.join(self.output_dir, "activities", activity_name, "screenshots")
                    #append number if existing activity
                    if activity_name in self.activity_list:
                        activity_name = activity_name + "_" + str(self.activity_list.count(activity_name))
                    self.activity_list.append(activity_name)
                #move json
                if json_dest:
                    shutil.copy(os.path.join(src, file), os.path.join(json_dest, activity_name + ".json"))
                #move image
                if os.path.exists(os.path.join(src, "screen" + file_name + "jpg")):
                    img_path = os.path.join(src, "screen" + file_name + "jpg")
                    shutil.copy(img_path, os.path.join(img_dest, activity_name + ".jpg"))
                    
                    
    def get_screenshots(self) -> str:
        """run xbot and droidbot and copy screenshots into activity folders"""
        activites_path = os.path.join(self.output_dir, "activities")
        if not os.path.exists(activites_path):
            os.makedirs(activites_path)
        exists = False
        if os.path.isdir(os.path.join(TEMP_PATH, "xbot")):
            self._move_files_xb("",True,False,True)
            exists = True
        if os.path.isdir(os.path.join(TEMP_PATH, "droidbot")): #xbot temp dir path
            self._move_files_db("",True, True)
            exists = True
        if not exists:
            xbot_task = Xbot()
            self.execute_task(xbot_task)
            droidbot_task = Droidbot()
            self.execute_task(droidbot_task)
            self.get_screenshot()
        return None