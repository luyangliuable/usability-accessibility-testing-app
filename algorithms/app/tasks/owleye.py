from tasks.task import Task
from resources.resource import *
from models.screenshot import Screenshot
from typing import List, Dict, Tuple
import os
import requests
import shutil
import json

class Owleye(Task):
    """Class for managing Owleye algorithm"""

    _input_types = [ResourceType.SCREENSHOT]
    _output_types = [ResourceType.DISPLAY_ISSUE]
    # _url = 'http://host.docker.internal:3004/execute'
    _url = os.environ['OWLEYE']
    _name = "Owleye"

    def __init__(self, output_dir, resource_groups : Dict[ResourceType, ResourceGroup], uuid: str) -> None:
        super().__init__(output_dir, resource_groups, uuid)
        self._thread=Thread(target=self.run)
        self.queue: list[Screenshot] = []         # list of unprocessed screenshots
        self.completed_states: set[str] = set()   # set of screenshot structure_ids that have been completed
        self._sub_to_screenshots()
        self.image_path=""

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
    def start(cls, image_dir, output_dir):
        """
        Signal start thread to the owleye.
        """
        task = Thread(target=cls.run, args=(image_dir, output_dir));
        task.start()


    @classmethod
    def run(cls, image_dir: str, output_dir: str) -> None:
        """Runs owleye algorithm for images in image_dir and outputs to output_dir"""
        data = {
            "image_dir" : image_dir,
            "output_dir" : output_dir
        }

        print(f'Starting {Owleye._name} with url {Owleye._url}')
        response = requests.post(Owleye._url, json=data, headers={"Content-Type": "application/json"})
        # response = Task.http_request(Owleye._url, data)

        status = 'SUCCESSFUL' if response and response.status_code==200 else 'FAILED'
        print(f'Status: { status }')


    def _process_images(self) -> None:
        """Runs owleye for images in queue and publishes results"""
        # copy images in queue to temp input directory
        temp_dir = os.path.join(self.output_dir, "tmp")

        try:
            os.makedirs(self.output_dir)
        except OSError:
            pass

        # TODO get temp file working

        # for screenshot in self.queue:
        print(self.image_path)
        shutil.copyfile(self.image_path, os.path.join( self.output_dir, "image.jpg" ))
        print(f'{temp_dir} created.')

        # run owleye algorithm and publish outputs
        Owleye.start(self.image_path, self.output_dir)
        self._publish_issues()

        # clear queue and input dir
        self.queue = []
        # shutil.rmtree(temp_dir)

    def _sub_to_screenshots(self) -> None:
        """Subscribe to screenshot resource group"""
        if ResourceType.SCREENSHOT in self.resource_dict:
            self.resource_dict[ResourceType.SCREENSHOT].subscribe(self._new_screenshot_callback)

    def _new_screenshot_callback(self, resource: ResourceWrapper) -> None:
        """Callback when a new screenshot is published"""
        screenshot = resource.get_metadata()
        self.image_path = resource.get_path()
        # if screenshot.structure_id not in self.completed_states:
        self.queue.append(screenshot)
        # self.completed_states.add(screenshot.structure_id)
        self._process_images()

    def _publish_issues(self) -> None:
        """Publish outputs to resource group"""
        if not ResourceType.DISPLAY_ISSUE in self.resource_dict:
            return

        print(f'Successfully ran owleye for image {self.image_path}')
        # issues = self._get_display_issues()
        # complete = False
        # for issue in issues:
        #     if issue == issues[-1]:
        #         complete = not self.resource_dict[ResourceType.SCREENSHOT].is_active()
        #     rw = ResourceWrapper(self.output_dir, 'Owleye', issue)
        #     self.resource_dict[ResourceType.DISPLAY_ISSUE].publish(rw, complete)

    def _get_display_issues(self) -> List[dict]:
        """Returns a list of heatmap images produced by owleye

        Returns:
            list[tuple(Screenshot, str)]: Pair of origial screenshot and heatmap image path
        """
        heatmaps = []
        for screenshot in self.queue:
            filename = os.path.basename(screenshot.get_image_jpeg())
            if os.path.exists(os.path.join(self.output_dir, filename)):
                heatmaps.append({"screenshot": screenshot,
                                 "image_path": os.path.join(self.output_dir, filename)
                                 })
        return heatmaps
