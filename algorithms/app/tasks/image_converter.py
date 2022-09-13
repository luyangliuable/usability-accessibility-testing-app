from PIL import Image
import json
import os
from resources.resource import ResourceGroup, ResourceWrapper
from tasks.task import Task

class ImageConverter(Task):
    
    def __init__(self, output_dir, dict, jpeg = False, png = False):
        super().__init__()
        self.output_dir = output_dir
        self.dict = dict
        self.jpeg_type = jpeg
        self.png_type = png


    @classmethod
    def get_name() -> str:
        return ImageConverter.__name__


    @classmethod
    def get_input_types(self) -> str:
        if self.jpeg_type:
            return "SCREENSHOT_PNG"
        if self.png_type:
            return "SCREENSHOT_JPEG"
        return None


    @classmethod
    def get_output_types(self) -> str:
        if self.jpeg_type:
            return "SCREENSHOT_JPEG"
        if self.png_type:
            return "SCREENSHOT_PNG"
        return None


    def execute(self):
        item_lst = self.dict[self.get_input_types()].get_all_resources()
        type_str = ''
        if self.jpeg_type:
            type_str = 'jpeg'
        elif self.png_type:
            type_str = 'png'
        
        for item in item_lst:
            #change file type
            path = item.get_path()
            item_json = json.loads(item.get_metadata())
            img1 = Image.open(path)
            file_base = os.path.basename(path)
            filename, file_extension = os.path.splitext(file_base)
            out_path = os.path.join(self.output_dir, filename + "." + type_str)
            img1.save(out_path)

            #update existing metadata
            item_json[type_str + " path"]: out_path
            item.set_metadata(item_json)

            #add new resource wrapper
            metadata = {
                "activity_name" : item_json['activity_name'],
            }
            resource = ResourceWrapper(out_path, item.get_origin(), json.dumps(metadata))
            rg = ResourceGroup(self.get_output_types(), None)
            rg.dispatch(resource, False)
    