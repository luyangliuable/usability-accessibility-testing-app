from PIL import Image
import json
import os
from resources import *
from tasks.task import Task
from typing import List

class ImageConverter(Task):
    
    def __init__(self, output_dir, dict, jpeg = False, png = False):
        super().__init__()
        self.output_dir = output_dir
        self.dict = dict
        self.jpeg_type = jpeg
        self.png_type = png


    def get_name() -> str:
        return ImageConverter.__name__


    def get_input_types(self) -> List[ResourceType]:
        if self.jpeg_type:
            return [ResourceType.SCREENSHOT_PNG]
        if self.png_type:
            return [ResourceType.SCREENSHOT_JPEG]
        return None


    def get_output_types(self) -> List[ResourceType]:
        if self.jpeg_type:
            return [ResourceType.SCREENSHOT_JPEG]
        if self.png_type:
            return [ResourceType.SCREENSHOT_PNG]
        return None


    def execute(self):
    
        type_str = ''
        if self.jpeg_type:
            type_str = 'jpeg'
        elif self.png_type:
            type_str = 'png'
        
        for type in self.get_input_types():
            item_lst = self.dict[type].get_all_resources()

            for item in item_lst:
                #change file type
                path = item.get_path()
                item_metadata = item.get_metadata()
                img1 = Image.open(path)
                img1 = img1.convert('RGB')
                out_path = os.path.join(self.output_dir, item_metadata.get_name() + "." + type_str)
                img1.save(out_path)

                #update existing metadata
                if self.jpeg_type:
                    item_metadata.set_jpeg_path(out_path)
                if self.png_type:
                    item_metadata.set_png_path(out_path)

                resource = ResourceWrapper(out_path, item.get_origin(), item_metadata)
                for item in self.get_output_types():
                    if item in self.dict:
                        rg = self.dict[item]
                        rg.dispatch(resource, False)
                    else:
                        rg = ResourceGroup(self.get_output_types(), None)
                        rg.dispatch(resource, False)

    