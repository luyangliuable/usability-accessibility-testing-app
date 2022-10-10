from tasks.task import Task
from resources.resource import *
from models.screenshot import Screenshot
from typing import List, Dict, Tuple
import os
import shutil

class Owleye(Task):
    """Class for managing Owleye algorithm"""
    
    name = "Owleye"
    _input_types = [ResourceType.SCREENSHOT]
    _output_types = [ResourceType.DISPLAY_ISSUE]
    _url = 'http://host.docker.internal:3004/execute'

    def __init__(self, output_dir, resource_groups : Dict[ResourceType, ResourceGroup], uuid: str) -> None:
        super().__init__(output_dir, resource_groups, uuid)
        self.queue: list[Screenshot] = []         # list of unprocessed screenshots
        self.completed_states: set[str] = set()   # set of screenshot structure_ids that have been completed
        self._sub_to_screenshots()

    @classmethod
    def get_name(cls) -> str:
        """Name of the task"""
        return Owleye.__name__
    
    @classmethod
    def get_input_types(cls) -> List[ResourceType]:
        """Input resource types of the task"""
        return Owleye._input_types

    @classmethod
    def get_output_types(cls) -> List[ResourceType]:
        """Output resource types of the task"""
        return Owleye._output_types
    
    @classmethod
    def run(cls, image_dir: str, output_dir: str) -> None:
        """Runs owleye algorithm for images in image_dir and outputs to output_dir"""
        data = {
            "image_dir" : image_dir,
            "output_dir" : output_dir
        }
        response = Task.http_request(Owleye._url, data)
        
        status = 'SUCCESSFUL' if response and response.status_code==200 else 'FAILED'
        print("STATUS " + status)
    
    def _process_images(self) -> None:
        """Runs owleye for images in queue and publishes results"""
        # copy images in queue to temp input directory
        temp_dir = os.path.join(self.output_dir, 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        for screenshot in self.queue:
            shutil.copy(screenshot.get_image_jpeg(), temp_dir)
        
        # run owleye algorithm and publish outputs
        Owleye.run(temp_dir, self.output_dir)
        self._publish_issues()

        # clear queue and input dir
        self.queue = []
        shutil.rmtree(temp_dir)
    
    def _sub_to_screenshots(self) -> None:
        """Subscribe to screenshot resource group"""
        if ResourceType.SCREENSHOT in self.resource_dict:
            self.resource_dict[ResourceType.SCREENSHOT].subscribe(self._new_screenshot_callback)
    
    def _new_screenshot_callback(self, resource: ResourceWrapper) -> None:
        """Callback when a new screenshot is published"""
        screenshot = resource.get_metadata()
        if screenshot.structure_id not in self.completed_states:
            self.queue.append(screenshot)
            self.completed_states.add(screenshot.structure_id)
            self._process_images()
    
    def _publish_issues(self) -> None:
        """Publish outputs to resource group"""
        issues = self._get_display_issues()
        complete = False
        for issue in issues:
            if issue == issues[:-1]:
                complete = not self.resource_dict[ResourceType.SCREENSHOT.is_active()]
            rw = ResourceWrapper(self.output_dir, self.get_name(), issue)
            self.resource_dict[ResourceType.DISPLAY_ISSUE].publish(rw, complete)
        
    def _get_display_issues(self) -> List[Tuple[Screenshot, str]]:
        """Returns a list of heatmap images produced by owleye
        
        Returns: 
            list[tuple(Screenshot, str)]: Pair of origial screenshot and heatmap image path
        """
        heatmaps = []
        for screenshot in self.queue:
            filename = os.path.basename(screenshot.get_image_jpeg())
            if os.path.exists(os.path.join(self.output_dir, filename)):
                heatmaps.append((screenshot, os.path.join(self.output_dir, filename)))
        return heatmaps