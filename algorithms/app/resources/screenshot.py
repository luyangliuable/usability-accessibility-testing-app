from typing import List, Callable
from resources import *

class Screenshot():
    
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
    
    def set_tappability_prediction(self, check) -> None:
        self.tappability_prediction = check
    
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
    
    def subscribe(self, subscriber : Callable[[str],None], type: str) -> None:
        """Subscriber for json"""
        self.subscribers.append(subscriber) # add subscriber to queue
        self._update_queue(type)
    
    def _update_queue(self, type:str) -> None:
        """Notifies next subscriber if json is exists"""
        # if there are more subscribers and emulator is free, notify the next
        if type == "json":
            check = self.json_path
        if len(self.subscribers) > 0 and check != "":  
            self.subscribers.pop(0)(self.img_name)
    
