import os
from resources.resource import *
from models.screenshot import *
from tasks.task import Task
from typing import List, Callable, Tuple
import shutil
import subprocess
import json
from tasks.enums.status_enum import *
from time import sleep

class Tappability(Task):
    """Class for managing Tappability algorithm"""
    
    _input_types = [ResourceType.SCREENSHOT]
    _output_types = [ResourceType.TAPPABILITY_PREDICTION]
    _url = "http://host.docker.internal:3007/execute"
    
    def __init__(self, output_dir: str, resource_dict: dict[ResourceType, ResourceGroup], uuid: str) -> None:
        super().__init__(output_dir, resource_dict, uuid)
        self.input_dir = os.path.join(self.output_dir, 'temp')
        self.queue: list[Screenshot] = []         # list of unprocessed screenshots
        self.completed_states: set[str] = set()   # set of screenshot structure_ids that have been completed
        self.threshold = 80
        self._sub_to_new_screenshots()
            
    @classmethod
    def get_name(cls) -> str:
        """Name of the task"""
        return cls.__name__
    
    @classmethod
    def get_input_types(cls) -> List[ResourceType]:
        return Tappability._input_types

    @classmethod
    def get_output_types(cls) -> List[ResourceType]:
        return Tappability._output_types

    @classmethod
    def run(cls, image_dir: str, json_dir: str, output_dir: str, threshold: int) -> StatusEnum:
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
        
        status = StatusEnum.successful if response and response.status_code==200 else StatusEnum.failed
        print("STATUS " + str(status))
        return status
    
    def is_complete(self) -> bool:
        return (len(self.queue) == 0 and not self.resource_dict[ResourceType.SCREENSHOT].is_active())
        
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
             if not self.status == StatusEnum.running:
                self.start()
             
    def start(self) -> None:
        """ Signal start thread for task."""
        if self.status == StatusEnum.running:
            return
        
        self.status = StatusEnum.running
        task = Thread(target=self._process_images);
        task.start()
        
    def _process_images(self) -> None:
        """Run Tappability on temp batch"""
        print(f'Starting Tappability. Status: {self.status}') 
        
        while self.status == StatusEnum.running:
            if self.is_complete():
                self.status = StatusEnum.successful
                break
            if len(self.queue) == 0:
                sleep(5.0)
                continue
            
            try:
                # get next screenshot from queue
                next_img = self.queue.pop(0)
                self._prepare_inputs([next_img])
                print(f'Running Tappability for {next_img}')
                response = Tappability.run(self.input_dir, self.input_dir, self.output_dir, self.threshold)
                result = self._get_results([next_img])
                if response == StatusEnum.successful and len(result) > 0:
                    print(f'Tappability successfully proccessed image: {next_img}. Output: {result[0]}\n')
                    self._publish(result)
            except Exception as err:
                print(f"Error {err} in Tappability while trying to process image.\Tappability continuing")
            
            
    def _prepare_inputs(self, images: list[Screenshot]) -> None:
        """Move ready items into temp directory"""
        if os.path.exists(self.input_dir):
            shutil.rmtree(self.input_dir)
        os.makedirs(self.input_dir)
        for img in images:
            img_path = img.get_image_jpeg()
            json_path = img.get_layout_json()
            shutil.copy(img_path, self.input_dir)
            # give json same filename as image
            img_filename = os.path.splitext(os.path.basename(img_path))[0]
            shutil.copy(json_path, os.path.join(self.input_dir, f'{img_filename}.json'))

    
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
            img_path = os.path.join(result_dir, 'screenshot.jpg')
            desc_path = os.path.join(result_dir, 'description.json')
            
            heatmap_paths = []
            for file in os.listdir(result_dir):
                if file[-5:] == 'description.json':
                    continue
                if file == 'screenshot.jpg':
                    continue
                heatmap_paths.append(os.path.join(result_dir, file))
            
            desc = []
            if os.path.exists(desc_path):
                with open(desc_path) as f:
                    desc_file = json.loads(f.read())
                    for item in dict(desc_file).values():
                        desc.append(item)     
            
            if not os.path.exists(img_path):
                img_path = screenshot.image_path
                                
            if img_path is not None and desc_path is not None:
                results.append({"screenshot": screenshot, 
                                "image_path": img_path, 
                                "description_path": desc_path,
                                "description": desc, 
                                "heatmaps": heatmap_paths
                                })
        return results       
        
    
    def _publish(self, item_lst: List[dict]) -> None:
        """publishes and updates item"""
        if not ResourceType.TAPPABILITY_PREDICTION in self.resource_dict:
            return
        
        for item in item_lst:
            print('tappable publishing ' + str(item))
            rw = ResourceWrapper(self.__class__.__name__, item)
            self.resource_dict[ResourceType.TAPPABILITY_PREDICTION].publish(rw, self.is_complete())
        
    

    def is_complete(self):
        """Checks if all images in list have been convertered and resource group is no longer active"""
        return len(self.queue) == 0 and not self.resource_dict[ResourceType.SCREENSHOT].is_active()