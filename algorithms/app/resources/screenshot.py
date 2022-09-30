# from tkinter import Image
from typing import List, Callable
from tasks.image_converter import ImageConverter
from tasks.layout_converter import LayoutConverter
import json

IMAGE_TYPE_PAIRING = {
    'png': 'jpeg',
    'jpeg': 'png'
}

LAYOUT_TYPE_PAIRING = {
    'json': 'xml'
}

class Screenshot():
    
    def __init__(self, view_name, output_dir, image_files ={}, layout_files = {}):
        self.view_name = view_name
        self.image_files = image_files
        self.layout_files = layout_files
        self.output_dir = output_dir
        self.tappability_dir = None
        
    def get_name():
        return Screenshot.__name__
        
    def get_view_name(self) -> str:
        return self.view_name
        
    def get_image_files(self) -> str:
        return self.image_files
        
    def add_image_file(self, type: str, file_path: str, update = False) -> None:
        if type not in self.image_files and type in IMAGE_TYPE_PAIRING.keys() or update:
            self.image_files[type] = file_path
            
    def get_layout_files(self) -> str:
        return self.layout_files

    def add_layout_files(self, type: str, file_path: str, update = False) -> None:
        if type not in self.layout_files or update:
            self.layout_files[type] = file_path
        
    def convert_image(self) -> None:
        for key in IMAGE_TYPE_PAIRING.keys():
            if key not in self.image_files and IMAGE_TYPE_PAIRING[key] in self.image_files:
                self.add_image_file(key, ImageConverter(self.output_dir,self.image_files[IMAGE_TYPE_PAIRING[key]], self.view_name, type = key).execute()) 
       
    def convert_layout(self) -> None:
        for key in LAYOUT_TYPE_PAIRING.keys():
            if key not in self.layout_files and LAYOUT_TYPE_PAIRING[key] in self.layout_files:
                self.add_layout_files(key, LayoutConverter(self.output_dir,self.layout_files[LAYOUT_TYPE_PAIRING[key]], self.view_name).execute()) 
       
    def get_tappability_path(self) -> str:
        return self.tappability_dir
    
    def set_tappability_path(self, path:str) -> None:
        self.tappability_dir = path
        
    def __str__(self) -> str:
        return json.dumps({
                   "view_name": self.view_name, 
                   "image_files": self.image_files,
                   "layout_files": self.layout_files
                   })
            

if __name__ == '__main__':
    sc = Screenshot('main', '/Users/em.ily/Desktop/temp', {'png': '/Users/em.ily/Desktop/temp/a2dp.Vol_.main.png'}, {'xml':'/Users/em.ily/Desktop/temp/xbot/screenshot/layouts/a2dp.Vol.main.xml'})
    sc.convert_layout()
    print(str(sc))
             

    # def __init__(self, img_name, activity_name, jpeg_path = "", png_path = "", xml_path = "", json_path = ""):
    #     self.tappability_prediction = False
    #     self.json_path = json_path
    #     self.xml_path = xml_path
    #     self.jpeg_path = jpeg_path
    #     self.png_path = png_path
    #     self.img_name = img_name
    #     self.activity_name = activity_name
    #     self.subscribers = []
        
    # def get_name(cls) -> str:
    #     return Screenshot._name__

    # def get_input_types(self) -> List[ResourceType]:
    #     return None

    # def get_output_types(self) -> List[ResourceType]:
    #     return None
    
    # def set_tappability_prediction(self, check) -> None:
    #     self.tappability_prediction = check
    
    # def get_tappability_prediction(self) -> bool: 
    #     return self.tappability_prediction

    # def set_json_path(self, json_path) -> None: 
    #     self.json_path = json_path

    # def get_json_path(self) -> str:
    #     return self.json_path

    # def set_jpeg_path(self, jpeg_path) -> None:
    #     self.jpeg_path = jpeg_path

    # def get_jpeg_path(self) -> str:
    #     return self.jpeg_path

    # def set_png_path(self, png_path) -> None:
    #     self.png_path = png_path

    # def get_png_path(self) -> str:
    #     return self.png_path

    # def get_xml_path(self) -> str:
    #     return self.xml_path

    # def get_img_name(self) -> str:
    #     return self.img_name

    # def get_activity_name(self) -> str:
    #     return self.activity_name
    
    # def subscribe(self, subscriber : Callable[[str],None], type: str) -> None:
    #     """Subscriber for json"""
    #     self.subscribers.append(subscriber) # add subscriber to queue
    #     self._update_queue(type)
    
    # def _update_queue(self, type:str) -> None:
    #     """Notifies next subscriber if json is exists"""
    #     # if there are more subscribers and emulator is free, notify the next
    #     if type == "json":
    #         check = self.json_path
    #     if len(self.subscribers) > 0 and check != "":  
    #         self.subscribers.pop(0)(self.img_name)
    
