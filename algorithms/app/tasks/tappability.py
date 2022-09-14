from PIL import Image
import json
import os
from resources.resource import ResourceGroup, ResourceWrapper
from resources.resource_types import ResourceType
from tasks.task import Task
from typing import List


class Tappability(Task):
    """Class for managing Tappability algorithm"""
    
    def __init__(self, output_dir, resource_dict, threshold = 50) -> None:
        super().__init__(output_dir, resource_dict)
        self._threshold = threshold
        self._image_lst = {}
        self._running = False


    def add_screenshot(self, screenshot: ResourceWrapper) -> None:
        if screenshot.get_jpeg_path() == "":
            screenshot.subscribe()
        else:
            self._image_lst[screenshot] = False
        

    def get_name() -> str:
        return Tappability.__name__


    def get_input_types(self) -> List[ResourceType]:
        return [ResourceType.SCREENSHOT_JPEG]


    def get_output_types(self) -> List[ResourceType]:
       return [ResourceType.TAPPABILITY_PREDICT]


    def execute(self) -> None:

        #TODO 
        # if not self._running: 


        # for type in self.get_input_types():
        #     item_lst = self.resource_dict[type].get_all_resources()

        #     for item in item_lst:

        #         item_metadata = item.get_metadata()
        #         item_path = item_metadata.get_jpeg_path()

        #         #checks if already executed - DO I STILL NEED THIS ???
        #         if not item_metadata.get_tappability_predict():
        #             filename = item_metadata.get_img_name()
        #             out_path = os.path.join(self.output_dir, filename)
        #             if not os.path.exists(out_path):
        #                 os.makedirs(out_path)

        #             #run pipeline
        #             json_path = item_metadata.get_json_path()
        #             if json_path:
        #                 self._pipeline(item_path , json_path, out_path, self._threshold)

        #             #update metadata
        #             item_metadata.set_tappability_predict(True)


        #             #create resourcewrapper
        #             resource = ResourceWrapper(out_path, item.get_origin(), item_metadata)
        #             for item in self.get_output_types():
        #                 if item in self.dict:
        #                     rg = self.dict[item]
        #                     rg.dispatch(resource, False)
        #                 else:
        #                     rg = ResourceGroup(self.get_output_types(), None)
        #                     rg.dispatch(resource, False)


