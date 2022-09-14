from task import *
from app.resources import *
from typing import List, Dict
import os
import sys

class Storydistiller(Task):
    """Class for managing Storydistiller algorithm"""
    
    _input_types = [ResourceType.APK_FILE, ResourceType.EMULATOR]
    _output_types = [ResourceType.SCREENSHOT_PNG, ResourceType.XML_LAYOUT]
    _url = 'http://host.docker.internal:3002'
    
    def __init__(self, output_dir, resource_dict : Dict[ResourceType, ResourceGroup]) -> None:
        super().__init__(output_dir, resource_dict)
        self.apks = {}
        self._sub_to_apks()

    def get_name() -> str:
        """Name of the task"""
        return Storydistiller.__name__
    
    def get_input_types() -> List[ResourceType]:
        """Input resource types of the task"""
        return Storydistiller._input_types

    def get_output_types() -> List[ResourceType]:
        """Output resource types of the task"""
        return Storydistiller._output_types
    
    @classmethod
    def run(cls, apk_path: str, output_dir: str, emulator: str) -> None:
        """Runs Storydistiller"""
        data = {
            "apk_path": apk_path,
            "output_dir": output_dir,
            "emulator": emulator
        }
        
        Storydistiller.http_request('http://host.docker.internal:3002/execute', data)
    
    
    def _sub_to_apks(self) -> None:
        """Get notified when a new APK is available"""
        if ResourceType.APK_FILE in self.resource_dict:
            self.resource_dict[ResourceType.APK_FILE].subscribe(self.apk_callback) # calls add_apk() when new apk is available
            
    def _sub_to_emulators(self) -> None:
        """Get notified when an emulator is available"""
        if ResourceType.EMULATOR in self.resource_dict:
            for resource in self.resource_dict[ResourceType.EMULATOR].get_all_resources():
                resource.get_metadata().subscribe(self.emulator_callback)
            
    
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
        
        
    def apk_callback(self, new_apk : ResourceWrapper) -> None:
        """callback method to add apk and run algorithm"""
        if new_apk.get_path() not in self.apks:
            self._add_apk(new_apk.get_path())
            self._process_apks()
        
    
    
    def emulator_callback(self, emulator) -> None:
        """callback method for using emulator"""
        
        self._process_apks(emulator=emulator)
        
if __name__ == '__main__':
    #TODO
    # create apk resource
    # create emulator resource
    # create storydistiller object
    # add apk
    
    
    # make resource groups
    apk_resources = ResourceGroup(ResourceType.APK_FILE)
    emulator_resources = ResourceGroup[Emulator](ResourceType.EMULATOR)
    resource_dict = {} # make resource dict
    resource_dict[ResourceType.APK_FILE] = apk_resources
    resource_dict[ResourceType.EMULATOR] = emulator_resources
    storydistiller = Storydistiller('/home/data/test_apks/a2dp.Vol_133/storydistiller/', resource_dict)
    
    apk = ResourceWrapper('/home/data/test_apks/a2dp.Vol_133/a2dp.Vol_133.apk', 'upload')
    emulator = ResourceWrapper('', 'upload', Emulator('host.docker.internal:5555'))
    
    emulator_resources.dispatch(emulator, False)
    apk_resources.dispatch(apk, False)