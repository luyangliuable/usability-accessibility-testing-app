from resources.screenshot import Screenshot
from tasks.task import *
from resources.resource import *
from typing import List, Dict
import os
from PIL import Image
import shutil

class Xbot(Task):
    """Class for managing Xbot algorithm"""
    
    _input_types = [ResourceType.APK_FILE, ResourceType.EMULATOR]
    _output_types = [Screenshot, ResourceType.ACCESSABILITY_ISSUE]
    _url = 'http://host.docker.internal:3003/execute'

    
    def __init__(self, output_dir, resource_dict : Dict[ResourceType, ResourceGroup]) -> None:
        super().__init__(output_dir, resource_dict)
        print("xbot")

        self.apk_queue = []

        self._sub_to_apks()
        self._sub_to_emulators()
        

    @classmethod
    def get_name(cls) -> str:
        """Name of the task"""
        return Xbot.__name__
    
    @classmethod
    def get_input_types(cls) -> List[ResourceType]:
        """Input resource types of the task"""
        return Xbot._input_types

    @classmethod
    def get_output_types(cls) -> List[ResourceType]:
        """Output resource types of the task"""
        return Xbot._output_types
    


    @classmethod
    def run(cls, apk_path: str, output_dir: str, emulator: str) -> None:
        """Runs Xbot"""
        data = {
            "apk_path": apk_path,
            "output_dir": output_dir,
            "emulator": emulator
        }
        
        Xbot.http_request(Xbot._url, data)
    
    def _sub_to_apks(self) -> None:
        """Get notified when a new APK is available"""
        if ResourceType.APK_FILE in self.resource_dict:
            self.resource_dict[ResourceType.APK_FILE].subscribe(self.apk_callback) # calls add_apk() when new apk is available
            
            
    def _sub_to_emulators(self) -> None:
        """Get notified when an emulator is available"""
        if ResourceType.EMULATOR in self.resource_dict:
            self.resource_dict[ResourceType.EMULATOR].subscribe(self.emulator_callback)
    
    
    def _process_apks(self, emulator) -> None:
        """Process apks"""
        
        print("XBOT RUNNING")

        while len(self.apk_queue) > 0:                              # get next apk
            apk = self.apk_queue.pop(0)

            apk_path = apk.get_path()
            emulator_path = emulator.get_path()
            Xbot.run(apk_path, self.output_dir, emulator_path)      # run algorithm
            self._dispatch_outputs()                                # dispatch results

            apk.release()

        print("XBOT COMPLETED")
        
    
    def _dispatch_outputs(self) -> None:
        """Dispatch all outputs for processed apk"""
        pass
    
    
    def _get_screenshots(self) -> List[str]:
        """Gets list of paths to all screenshots in output_path"""
        pass
    
    def _get_layouts(self) -> List[str]:
        """Gets list of paths to all layouts in output_path"""
        pass
    
    def _get_display_issues(self) -> List[str]:
        """Gets list of dir paths to each issue"""
        pass
    
    def apk_callback(self, new_apk : ResourceWrapper) -> None:
        """callback method to add apk and run algorithm"""
        if new_apk not in self.apk_queue:
            self.apk_queue.append(new_apk)

    
    def emulator_callback(self, emulator : ResourceWrapper) -> None:
        """callback method for using emulator"""
        
        self._process_apks(emulator=emulator)
        emulator.release()
    
    
    def is_complete(self) -> bool:
        pass
        # return if subscriptions are complete and apk list is empty
        
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
