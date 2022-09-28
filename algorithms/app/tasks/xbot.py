from resources.screenshot import Screenshot
from tasks.task import *
from resources.resource import *
from typing import List, Dict, Tuple
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
        screenshots = self._get_screenshots()
        issues = self._get_accessibility_issues()
        
    
    
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
    

    def _get_screenshots(self) -> List[Tuple[str, str, str]]:
        """ Gets list of screenshot images and layouts from xbot output directory.
            Returns list of tuples containing (activity name, image path, layout path)
        """
        screenshots = []
        images_dir = os.path.join(self.output_dir, "screenshot")     
        layouts_dir = os.path.join(self.output_dir, "layouts")
        
        for activity in os.listdir(images_dir):
            layout_path = os.path.join(layouts_dir, activity + ".xml")
            # select image file which is not the thumbnail 
            for filename in os.path.join(images_dir, activity):
                if len(filename) > 14 and filename[-14:-5] != "_thumbnail":
                    image_path = os.path.join(images_dir, activity, filename)
                    screenshots.append((activity, image_path, layout_path))
                    break      
        return screenshots
        
    def _get_accessibility_issues(self) -> List[Tuple[str, str, str]]:
        """ Gets list of accessibility issues from xbot output directory. 
            Returns list of tuples containing (activity name, image path, description path)        
        """
        issues = []
        issues_dir = os.path.join(self.output_dir, "issues")

        # folder name = activity name 
        for activity in os.listdir(issues_dir):                    
            image_path = os.path.join(issues_dir, activity, activity + ".png")
            desc_path = os.path.join(issues_dir, activity, activity + ".txt")
            if os.path.exists(image_path) and os.path.exists(desc_path):
                issues.append((activity, image_path, desc_path))             
        return issues
