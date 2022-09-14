from typing import List, Callable
from task import Task
from resources import *

class Screenshot(Task):
    
    def __init__(self, img_name, activity_name, jpeg_path = "", png_path = "", xml_path = "", json_path = ""):
        self.tappability_prediction = False
        self.json_path = json_path
        self.xml_path = xml_path
        self.jpeg_path = jpeg_path
        self.png_path = png_path
        self.img_name = img_name
        self.activity_name = activity_name
        self.subscribers = []
        
    def get_name() -> str:
        return Screenshot._name__

    def get_input_types(self) -> List[ResourceType]:
        return None

    def get_output_types(self) -> List[ResourceType]:
        return None
    
    def add_tappability_prediction(self) -> None:
        self.tappability_prediction = True
    
    def get_tappability_prediction(self) -> bool: 
        return self.tappability_prediction

    def set_json_path(self, json_path) -> None: 
        self.json_path = json_path

    def get_json_path(self) -> str:
        return self.json_path

    def set_jpeg_path(self, jpeg_path) -> None:
        self.jpeg_path = jpeg_path

    def get_jpeg_path(self) -> str:
        return self.jpeg_path

    def set_png_path(self, png_path) -> None:
        self.png_path = png_path

    def get_png_path(self) -> str:
        return self.png_path

    def get_xml_path(self) -> str:
        return self.xml_path

    def get_img_name(self) -> str:
        return self.img_name

    def get_activity_name(self) -> str:
        return self.activity_name
    
