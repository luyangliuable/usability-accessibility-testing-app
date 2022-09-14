from typing import List, Callable
from tasks.task import Task

class Screenshot(Task):
    def __init__(self, img_name, activity_name, jpeg_path = "", png_path = "", xml_path = "", json_path = ""):
        self._tappability_prediction = False
        self._json_path = json_path
        self._xml_path = xml_path
        self._jpeg_path = jpeg_path
        self._png_path = png_path
        self.img_name = img_name
        self.activity_name = activity_name


    def subscribe(self, subscriber : Callable(str)) -> None:
        """Subscriber for emulator"""
        self.subscribers.append(subscriber) # add subscriber to queue
        self._update_queue()

    # def _update_queue(self) -> None:
    #     """Notifies next subscriber if emulator is free"""
    #     # if there are more subscribers and emulator is free, notify the next
    #     if len(self.subscribers) > 0:  
    #         self.subscribers.pop(0)(self.name)
    #         self.is_free = False
        
    
    def add_tappability_prediction(self) -> None:
        self._tappability_prediction = True
    
    def get_tappability_prediction(self) -> bool: 
        return self._tappability_prediction

    def set_json_path(self, json_path) -> None: 
        self._json_path = json_path

    def get_json_path(self) -> str:
        return self._json_path

    def set_jpeg_path(self, jpeg_path) -> None:
        self._jpeg_path = jpeg_path

    def get_jpeg_path(self) -> str:
        return self._jpeg_path

    def set_png_path(self, png_path) -> None:
        self._png_path = png_path

    def get_png_path(self) -> str:
        return self._png_path

    def get_xml_path(self) -> str:
        return self._xml_path

    def get_img_name(self) -> str:
        return self._img_name

    def get_activity_name(self) -> str:
        return self._activity_name
    
