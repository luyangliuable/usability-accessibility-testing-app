from algorithm_controllers import *
import os
import json
import shutil
from xml_converter import xmlConverter
from PIL import Image

TEMP_PATH = ""

class ApkDetails:
    
    def __init__(self, apk_path, output_dir) -> None:
        self.apk_path = apk_path
        self.output_dir = output_dir
        self.tasks = {}
        self.activity_list = []
    
    def _init_output_dir(self) -> None:
        """Initialises ouput directory and creates temp directory for processing"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(TEMP_PATH):
            os.makedirs(TEMP_PATH)
    
    def execute_task(self, task: Task) -> None:
        """Executes task"""
        task_name = task.get_name()
        if task_name not in self.tasks:
            task.execute()
            self.tasks[task_name] = task

    
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

    def _move_files_xb(self, img_dest, json_dest=None, jpg= False, activity= False):
        """Moves xbot image and xml files from xbot temp file to dest. Reformats xml files to json."""
        img_src = os.path.join(TEMP_PATH,"xbot", "screenshot")
        xml_src = os.path.join(TEMP_PATH,"xbot", "screenshot","layouts")
        activites_path = os.path.join(self.output_dir, "activities")
        for subdir, dir, files in os.walk(img_src):
            for file in files:
                if file.endswith('.png'):
                    activity_name = subdir.split('/')[-1]
                    if activity_name not in ['screenshot', 'layouts']:
                        if activity:
                            if not os.path.exists(os.path.join(activites_path, activity_name)):
                                os.makedirs(os.path.join(activites_path, activity_name))
                                os.makedirs(os.path.join(activites_path, activity_name, "screenshots"))
                                os.makedirs(os.path.join(activites_path, activity_name, "annotations"))
                            img_dest = os.path.join(self.output_dir, "activities", activity_name, "screenshots")
                            json_dest = os.path.join(self.output_dir, "activities", activity_name, "annotations")
                        #convert xml to json & move to json directory
                        if json_dest:
                            xml_path = os.path.join(xml_src, activity_name + '.xml')
                            json_path = os.path.join(json_dest, activity_name + ".json")
                            xml_conv = xmlConverter(xml_path, json_path)
                            xml_conv.convert_xml_to_json()                            
                        #append count if mulitple
                        if activity_name in self.activity_list:
                            acitivity_name = activity_name + "_" + str(self.activity_list.count(acitivity_name))
                        #convert to jpg & save/copy file to dest
                        if jpg:
                            im1 = Image.open(os.path.join(subdir, file))
                            im1.save(os.path.join(img_dest, activity_name + '.jpg'))
                        else:
                            shutil.copy(os.path.join(subdir, file), os.path.join(img_dest, activity_name + '.png'))


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
    
    def _run_image_algorithms(self, xbot=True, droidbot=True):
        """Run xbot and droidbot (screenshot algorithms)"""
        if xbot and 'xbot' not in self.tasks:
            xbot_task = Xbot() #check inputs
            self.execute_task(xbot_task)
        if droidbot and 'droidbot' not in self.tasks:
            droidbot_task = droidbot() #check inputs
            self.execute_task(droidbot_task)

    def get_accessibility_issues(self) -> str:
        # run xbot and droidbot if not already run
        self._run_image_algorithms(droidbot = False)
        # copy results into activity folders
        xbot_path = os.path.join(TEMP_PATH, "xbot", "issues")
        activites_path = os.path.join(self.output_dir, "activities")
        for folder in os.listdir(xbot_path):
            dir_path = os.path.join(activites_path, folder)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            activity_folder_path = os.path.join(dir_path, "accessibility_issues")
            print(activity_folder_path)
            if not os.path.exists(activity_folder_path):
                os.makedirs(activity_folder_path)
            for file in os.listdir(os.path.join(xbot_path, folder)):
                if file.endswith('.txt') or file.endswith('.png'):
                    src_path = os.path.join(xbot_path, folder, file)
                    shutil.copy(src_path, activity_folder_path)
        return None

    
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
    
    def get_tappability_predictions(self) -> str:
        # run xbot and droidbot if not already run
        self._run_image_algorithms()
        # copy screenshots into temp folder convert PNGs to JPEG & get annotations
        img_path = os.path.join(TEMP_PATH,"tappability", "screenshots")
        json_path = os.path.join(TEMP_PATH,"tappability", "annotations")
        self._move_files_xb(img_path, json_path, jpg=True)
        self._move_files_db(img_path, json_path)
        # run tappability
        tappability = Tappability(img_path, json_path, os.path.join(self.output_dir,"tappability"), threshold=50)
        self.execute_task(tappability)
        # copy results into activity folders
        self._get_ui_display_issues(tappability=True)
        return None
    
    def get_execution_trace(self) -> str:
        # run droidbot
        self._run_image_algorithms(xbot=False)
        # copy utg into gifdroid input folder
        img_path = os.path.join(TEMP_PATH,"gifdroid")
        # run gifdroid
        gifdroid = Gifdroid() #check path
        self.execute_task(gifdroid)
        return None
   

if __name__=='__main__':
    pass