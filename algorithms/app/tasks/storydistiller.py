from tasks.task import Task
from resources import *
from typing import List, Dict
import os

class Storydistiller(Task):
    """Class for managing Storydistiller algorithm"""
    
    _input_types = [ResourceType.APK_FILE, ResourceType.EMULATOR]
    _output_types = [ResourceType.SCREENSHOT_PNG, ResourceType.XML_LAYOUT]
    _url = 'http://host.docker.internal:3002'
    
    def __init__(self, output_dir, resource_dict : Dict[ResourceType, ResourceGroup]) -> None:
        super().__init__(output_dir, resource_dict)
        self.apks = {}
        self._sub_to_apks()

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
    
    @classmethod
    def run(apk_path: str, output_dir: str, emulator: str) -> None:
        """Runs Storydistiller"""
        data = {
            "apk_path": apk_path,
            "output_dir": output_dir,
            "emulator": emulator
        }
        
        Storydistiller.http_request(url=Storydistiller._url, data=data)
    
    
    def _sub_to_apks(self) -> None:
        """Get notified when a new APK is available"""
        if ResourceType.APK_FILE in self.resource_dict:
            self.resource_dict[ResourceType.APK_FILE].subscribe(self.new_apk_callback) # calls add_apk() when new apk is available
            
    def _sub_to_emulators(self) -> None:
        """Get notified when an emulator is available"""
        if ResourceType.EMULATOR in self.resource_dict:
            for resource in self.resource_dict[ResourceType.EMULATOR].get_all_resources():
                resource.get_metadata().subscribe(self.emulator_callback())
            
    
    def _add_apk(self, apk_path) -> None:
        """Add new apk"""
        if apk_path not in self.apks:
            self.apks[apk_path] = False
    
    
    def _get_next(self) -> str:
        apks = [apk_path for apk_path, is_complete in self.apks.items() if not is_complete] # get unprocessed apks  
        return apks[0] if len(apks[0]) > 0 else None
    
    
    def _process_apks(self, emulator=None) -> None:
        """Process apks"""
        if emulator is None: # if there is no emulator, subscribe to emulators
            self._sub_to_emulators()
            return
        
        apk_path = self._get_next() # get next apk
        Storydistiller.run(apk_path, self.output_dir, emulator) # run algorithm
        self.apks[apk_path] = True  # set complete
        
        
    def apk_callback(self) -> None:
        """callback method to add apk and run algorithm"""
        for apk in self.resource_dict[ResourceType.APK_FILE].get_all_resources():
            if apk.get_path() not in self.apks:
                self._add_apk(apk.get_path())
    
    
    def emulator_callback(self, emulator) -> None:
        """callback method for using emulator"""
        self._process_apks(emulator=emulator)
        
        