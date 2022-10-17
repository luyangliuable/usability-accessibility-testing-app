from tasks.task import Task
from resources.resource import *
from models.screenshot import Screenshot
from typing import List, Dict, Tuple
import os
import requests
import shutil
import json
from tasks.enums.status_enum import *
from time import sleep

class Owleye(Task):
    """Class for managing Owleye algorithm"""

    _input_types = [ResourceType.SCREENSHOT]
    _output_types = [ResourceType.DISPLAY_ISSUE]
    # _url = 'http://host.docker.internal:3004/execute'
    _url = os.environ['OWLEYE']
    _name = "Owleye"

    def __init__(self, output_dir, resource_groups : Dict[ResourceType, ResourceGroup], uuid: str) -> None:
        super().__init__(output_dir, resource_groups, uuid)
        self.queue: list[Screenshot] = []         # list of unprocessed screenshots
        self.completed_states: set[str] = set()   # set of screenshot structure_ids that have been completed
        self.input_dir = os.path.join(self.output_dir, 'temp')
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
    def run(cls, image_dir: str, output_dir: str) -> StatusEnum:
        """Runs owleye algorithm for images in image_dir and outputs to output_dir"""
        data = {
            "image_dir" : image_dir,
            "output_dir" : output_dir
        }

        print(f'Starting {Owleye._name} with url {Owleye._url}')
        response = requests.post(Owleye._url, json=data, headers={"Content-Type": "application/json"})

        status = StatusEnum.successful if (response and response.status_code == 200) else StatusEnum.failed
        print(f'Status: { status }')
        return status
        

    def is_complete(self) -> bool:
        return (len(self.queue) == 0 and not self.resource_dict[ResourceType.SCREENSHOT].is_active())
        
    def start(self) -> None:
        """
        Signal start thread to the owleye.
        """
        if self.status == StatusEnum.running:
            return
        
        self.status = StatusEnum.running
        task = Thread(target=self._process_images);
        task.start()


    def _process_images(self) -> None:
        """Runs owleye for images in queue and publishes results"""
        print(f'Starting Owleye. Status: {self.status}') 
                   
        while self.status == StatusEnum.running:
            if self.is_complete():
                    self.status = StatusEnum.successful
                    break
            if len(self.queue) == 0:
                sleep(5.0)
                continue
            
            # run next image in queue
            try:
                next_img = self.queue.pop(0)
                self._prepare_inputs([next_img])
                print(f'Running Owleye for {next_img}')
                response = Owleye.run(self.input_dir, self.output_dir)
                result = self._get_display_issues([next_img])
                if response == StatusEnum.successful and len(result) > 0:
                    print(f'Owleye successfully proccessed image: {next_img}. Output: {result[0]}\n')
                    self._publish_issues(result)
            except Exception as err:
                print(f"Error {err} in Owleye while trying to process image.\nOwleye continuing")
            
    
    def _prepare_inputs(self, images: list[Screenshot]) -> None:
        """Moves screenshot jpeg images to input directory."""        
        # create temp input directory if it does not exist
        if os.path.exists(self.input_dir):
            shutil.rmtree(self.input_dir)            
        os.makedirs(self.input_dir)
        # try:
        #     os.makedirs(temp_dir)
        # except OSError:
        #     pass

        # copy screenshots to temp directory
        for img in images:
            img_path = img.get_image_jpeg()
            temp_path = os.path.join(self.input_dir, os.path.basename(img_path))
            shutil.copyfile(img_path, temp_path)

    def _sub_to_screenshots(self) -> None:
        """Subscribe to screenshot resource group"""
        if ResourceType.SCREENSHOT in self.resource_dict:
            self.resource_dict[ResourceType.SCREENSHOT].subscribe(self._new_screenshot_callback)

    def _new_screenshot_callback(self, resource: ResourceWrapper) -> None:
        """Callback when a new screenshot is published"""
        screenshot: Screenshot = resource.get_metadata()
        if screenshot.structure_id not in self.completed_states:
            self.queue.append(screenshot)
            self.completed_states.add(screenshot.structure_id)
            if not self.status == StatusEnum.running:
                self.start()

    def _publish_issues(self, issues: list[dict]) -> None:
        """Publish issues to resource group"""
        if not ResourceType.DISPLAY_ISSUE in self.resource_dict:
            return

        for issue in issues:
            rw = ResourceWrapper(issue["image_path"], 'Owleye', issue)
            self.resource_dict[ResourceType.DISPLAY_ISSUE].publish(rw, self.is_complete())

    def _get_display_issues(self, screenshots: list[Screenshot]) -> List[dict]:
        """Returns a list of heatmap images produced by owleye screenshots in params list

        Returns:
            list[tuple(Screenshot, str)]: Pair of origial screenshot and heatmap image path
        """
        heatmaps = []
        for screenshot in screenshots:
            filename = os.path.basename(screenshot.get_image_jpeg())
            if os.path.exists(os.path.join(self.output_dir, filename)):
                heatmaps.append({"screenshot": screenshot,
                                 "image_path": os.path.join(self.output_dir, filename)
                                 })
        return heatmaps
