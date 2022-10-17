import os
from resources.resource import *
from models.screenshot import *
from tasks.task import Task
from typing import List, Callable, Tuple
import shutil
import subprocess
import json

class Tappability(Task):
    """Class for managing Tappability algorithm"""
    
    _input_types = [ResourceType.SCREENSHOT]
    _output_types = [ResourceType.TAPPABILITY_PREDICTION]
    _url = "http://host.docker.internal:3007/execute"
    
    def __init__(self, output_dir: str, resource_dict: dict[ResourceType, ResourceGroup], uuid: str) -> None:
        super().__init__(output_dir, resource_dict, uuid)
        self.running = False
        self.queue: list[Screenshot] = []         # list of unprocessed screenshots
        self.completed_states: set[str] = set()   # set of screenshot structure_ids that have been completed
        self.threshold = 50
        self._sub_to_new_screenshots()
    
    @classmethod
    def __name__(cls) -> str:
        return "Tappable"
        
    @classmethod
    def get_name(cls) -> str:
        """Name of the task"""
        return Tappability.__name__
    
    @classmethod
    def get_input_types(cls) -> List[ResourceType]:
        return Tappability._input_types

    @classmethod
    def get_output_types(cls) -> List[ResourceType]:
        return Tappability._output_types

    @classmethod
    def run(cls, image_dir: str, json_dir: str, output_dir: str, threshold: int) -> None:
        """Runs Tappability algorithm.
        
        Attributes:
            image_dir: Dir with screenshot JPEG images.
            json_dir: Dir with JSON layout files with same filename as corresponding screenshot image.
            output_dir: Output dir.
            threshold: Min Tappability rating for an UI element to be considered tappable.
        """
        data = {
            "image_dir" : image_dir,
            "json_dir" : json_dir,
            "output_dir" : output_dir,
            "threshold" : str(threshold)
        }
        
        response = Tappability.http_request(Tappability._url, data)
        
        status = 'SUCCESSFUL' if response and response.status_code==200 else 'FAILED'
        print("STATUS " + status)
        
        
    def _sub_to_new_screenshots(self) -> None:
        """Get notified when new activity is added"""
        if ResourceType.SCREENSHOT in self.resource_dict:
            self.resource_dict[ResourceType.SCREENSHOT].subscribe(self.new_screenshot_callback)
    
    def new_screenshot_callback(self, resource: ResourceWrapper) -> None:
         """Callback method when new screenshot is added"""
         screenshot: Screenshot = resource.get_metadata()
         if screenshot.image_path is None or screenshot.layout_path is None:  # both image and layout required
             return
         if screenshot.structure_id not in self.completed_states:   # only add if similar UI structure not in list
             self.queue.append(screenshot)
             self.completed_states.add(screenshot.structure_id)
             self._run()
        
    def _run(self) -> None:
        """Run tappable on temp batch"""
        if self.running:
            return
        
        self.running = True
        path = os.path.join(self.output_dir + "temp")
        items = self._move_items(path)
        
        # run tappable
        Tappability.run(path, path, self.output_dir, self.threshold)
        
        # generate and publish result data
        result_list = self._get_results(items)
        self.queue = [img for img in self.queue if img not in items]    # update queue
        self._publish(result_list)
        shutil.rmtree(path)
        self.running = False
    
    def _move_items(self, path: str) -> list[Screenshot]:
        """Move ready items into temp directory"""
        if not os.path.exists(path):
            os.makedirs(path)
        item_ready = []
        for screenshot in self.queue:
            shutil.copy(screenshot.get_image_jpeg(), path)
            # give json same filename as image
            img_filename = os.path.splitext(os.path.basename(screenshot.image_path))[0]
            shutil.copy(screenshot.get_layout_json(), os.path.join(path, img_filename + ".json"))
            item_ready.append(screenshot)
        return item_ready
    
    def _get_results(self, screenshots: List[Screenshot]) -> List[dict]:
        """Get Tapability results for a list of screenshots. 
        
        Returns: 
            List[Tuple[Screenshot, str, str, List[str]]]: \
            original screenshot, annotated image path, rating description json path, list of heatmap image paths
        """
        results = []
        for screenshot in screenshots:
            img_name = os.path.splitext(os.path.basename(screenshot.image_path))[0]
            result_dir = os.path.join(self.output_dir, img_name)
            if not os.path.exists(result_dir):
                continue
            img_path = None
            desc_path = None
            heatmap_paths = []
            for file in os.listdir(result_dir):
                if file[-5:] == '.json':
                    desc_path = os.path.join(result_dir, file)
                    continue
                if file == 'screenshot.jpg':
                    img_path = os.path.join(result_dir, file)
                    continue
                heatmap_paths.append(os.path.join(result_dir, file))
                
            if img_path is not None and desc_path is not None:
                results.append({"screenshot": screenshot, 
                                "image_path": img_path, 
                                "description_path": desc_path, 
                                "heatmaps": heatmap_paths
                                })
        return results       
        
    
    def _publish(self, item_lst: List) -> None:
        """publishes and updates item"""
        if not ResourceType.TAPPABILITY_PREDICTION in self.resource_dict:
            return
        
        for item in item_lst:
            rw = ResourceWrapper(os.path.dirname(item[1]), self.get_name(), item)
            self.resource_dict[ResourceType.TAPPABILITY_PREDICTION].publish(rw, self.is_complete())
        
    

    def is_complete(self):
        """Checks if all images in list have been convertered and resource group is no longer active"""
        return len(self.queue) == 0 and not self.resource_dict[ResourceType.SCREENSHOT].is_active()