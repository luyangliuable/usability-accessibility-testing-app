from tasks.task import Task
from resources.resource import *
from models.screenshot import Screenshot
from typing import List
import os

class Owleye(Task):
    """Class for managing Owleye algorithm"""
    
    name = "Owleye"
    _input_types = [ResourceType.SCREENSHOT]
    _output_types = [ResourceType.DISPLAY_ISSUE]
    _url = 'http://host.docker.internal:3003/execute'

    def __init__(self, output_dir, resource_groups : Dict[ResourceType, ResourceGroup], uuid: str) -> None:
        super().__init__(output_dir, resource_groups, uuid)
        self.queue = {}

        
    @classmethod
    def run(image_dir: str, output_dir: str) -> None:
        data = {
            "image_dir" : image_dir,
            "output_dir" : output_dir
        }
        response = Task.http_request(url=Owleye._url, data=data)
        
        status = 'SUCCESSFUL' if response and response.status_code==200 else 'FAILED'
        print("STATUS " + status)
    
    
    def _process_images(self) -> None:
        temp_dir = os.path.join(self.output_dir, 'temp')
        screenshots = []
        for screenshot in self.queue.keys():
            if not self.queue[screenshot]:
                screenshots.append(screenshot)
        Owleye.run(screenshot.get_image_jpeg, self.output_dir)
        
        for screenshot in screenshots:
            self.queue[screenshot] = True
        
        self._publish_issues
        
    def _sub_to_screenshots(self) -> None:
        if ResourceType.SCREENSHOT in self.resource_dict:
            self.resource_dict[ResourceType.SCREENSHOT].subscribe(self.new_screenshot_callback)
    
    
    def _new_screenshot_callback(self, screenshot: Screenshot) -> None:
        self.queue[screenshot] = False
        self._process_images()
    
    
    def _publish_issues(self) -> None:
        issues = self._get_display_issues()
        resource_group = self.resource_dict[ResourceType.DISPLAY_ISSUE]
        complete = not self.resource_dict[ResourceType.SCREENSHOT.is_active()]
        for issue in issues:
            resource_group.publish(issue, complete)
        
    def _get_display_issues(self) -> list[tuple(str, str)]:
        """Returns a list of heatmap images produced by owleye"""
        issues = []
        for heatmap in os.listdir(self.output_dir):
            for image in self.queue.keys():
                if image.name == heatmap[:-4] and not self.queue[image]:
                    issues.append((image, os.path.join(self.output_dir, heatmap)))
            
        return issues