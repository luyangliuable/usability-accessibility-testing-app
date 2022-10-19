from tasks.task import Task
from resources.resource import *


class UiChecker(Task):
    """Class to manage ui-checker algorithm"""
    
    _input_types = [ResourceType.APK_FILE, ResourceType.UI_RULES]
    _output_types = [ResourceType.UI_FACTS]
    
    def __init__(self, output_dir: str, resource_dict: Dict[ResourceType, ResourceGroup], uuid: str) -> None:
        super().__init__(output_dir, resource_dict, uuid)
        
    @classmethod
    def run(cls, apk_path: str, rules_path: str, output_dir: str) -> None:
        pass
    
    @classmethod
    def get_input_types(cls) -> List[ResourceType]:
        return UiChecker._input_types
    
    @classmethod
    def get_output_types(cls) -> List[ResourceType]:
        return UiChecker._output_types
    
