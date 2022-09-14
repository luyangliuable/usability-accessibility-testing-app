from tasks.task import *
from resources.resource import *
from resources.emulator import *
from typing import List, Dict
import os

class Xbot(Task):
    """Class for managing Xbot algorithm"""
    
    _input_types = [ResourceType.APK_FILE, ResourceType.EMULATOR]
    _output_types = [ResourceType.SCREENSHOT_PNG, ResourceType.XML_LAYOUT, ResourceType.ACCESSABILITY_ISSUE]
    _url = 'http://host.docker.internal:3003/execute'

    
    def __init__(self, output_dir, resource_dict : Dict[ResourceType, ResourceGroup]) -> None:
        super().__init__(output_dir, resource_dict)

        self.apk_queue = []

        self._sub_to_apks()
        self._sub_to_emulators()



    @classmethod
    def get_name() -> str:
        """Name of the task"""
        return Xbot.__name__
    
    @classmethod
    def get_input_types() -> List[ResourceType]:
        """Input resource types of the task"""
        return Xbot._input_types

    @classmethod
    def get_output_types() -> List[ResourceType]:
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

        #    for resource in self.resource_dict[ResourceType.EMULATOR].get_all_resources():
        #        resource.get_metadata().subscribe(self.emulator_callback)
    
    
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

    
    def emulator_callback(self, emulator : ResourceWrapper[Emulator]) -> None:
        """callback method for using emulator"""
        
        self._process_apks(emulator=emulator)
        emulator.release()
    
    
    def is_complete(self) -> bool:
        pass
        # return if subscriptions are complete and apk list is empty
        
if __name__=='__main__':
    apk_resources = ResourceGroup(ResourceType.APK_FILE)
    emulator_resources = ResourceGroup[Emulator](ResourceType.EMULATOR)
    resource_dict = {} # make resource dict
    resource_dict[ResourceType.APK_FILE] = apk_resources
    resource_dict[ResourceType.EMULATOR] = emulator_resources
    
    storydistiller = Storydistiller('/home/data/test_apks/a2dp.Vol_133/storydistiller/', resource_dict)
    xbot = Xbot('/home/data/test_apks/a2dp.Vol_133/xbot/', resource_dict)
    
    apk = ResourceWrapper('/home/data/test_apks/a2dp.Vol_133/a2dp.Vol_133.apk', 'upload')
    emulator = ResourceWrapper('', 'upload', Emulator('host.docker.internal:5555'))
    
    emulator_resources.dispatch(emulator, False)
    apk_resources.dispatch(apk, False)