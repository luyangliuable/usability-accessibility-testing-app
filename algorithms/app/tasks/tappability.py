from urllib import response
from PIL import Image
import json
import os
from resources.resource import *
from resources.screenshot import *
from tasks.task import Task
from typing import List, Callable, Tuple
import shutil
import subprocess

class Tappability(Task):
    """Class for managing Tappability algorithm"""
    
    def __init__(self, output_dir, resource_dict, threshold) -> None:
        super().__init__(output_dir, resource_dict)
        self.img_lst = {}
        self.running = False
        input_type_img = self.get_input_types(cls)[0]
        self.threshold = threshold
        self._sub_to_unique_pairs()

        self.pairs = {}
        

    @classmethod
    def get_name(cls) -> str:
        return Tappability._name__

    @classmethod
    def get_input_types(cls) -> List[ResourceType]:
        return [ResourceType.SCREENSHOT_UNIQUEPAIR]

    @classmethod
    def get_output_types(cls) -> List[ResourceType]:
       return [ResourceType.TAPPABILITY_PREDICT]


   
    def _sub_to_unique_pair(self) -> None:
        """Get notified when new img/json is added"""
        self.resource_dict[ResourceType.SCREENSHOT_UNIQUEPAIR].subscribe(tappable_callback) 


    
    def tappable_callback(self, resource : ResourceWrapper[Tuple[ResourceWrapper, ResourceWrapper[Screenshot]]]) -> None:
        (jpeg, json) = resource.get_metadata(); 
        
        # TODO execute tappability with the provided JPEG and JSON
        return

                
    # def tappable_callback(self, new_img: ResourceWrapper) -> None:
    #      """Callback method to add img and run converter method"""
    #      if new_img.get_path() not in self.img_lst:
    #          self._add_img(new_img)
    #          self._process_img()

    def _add_img(self, img: ResourceWrapper) -> None:
        """Add img to img list"""
        img_path = img.get_path()
        if img_path not in self.img_lst:
            self.img_lst[img_path] = {"item": img, "is_completed": False, "ready": False}
            
    def _get_next(self) -> ResourceWrapper:
        """Get next img from list which is uncompleted"""
        img_lst = [val["item"] for val in self.img_lst.values() if not val["is_completed"] and not val["item"].get_metadata().get_tappability_prediction()]
        return img_lst[0] if len(img_lst) > 0 else None

    def _process_img(self) -> None:
        """Check to see if json is available. Process image or subscribe to json"""
        next_img = self._get_next()
        img_metadata = next_img.get_metadata()
        if img_metadata.get_json_path() == "":
            self._sub_to_json()
            return
        self.img_lst[next_img.get_path()]["ready"] = True # set ready
        self._run()
    
    
    def _sub_to_json(self) -> None:
        """Subscribe to screenshot json"""
        if ResourceType.JSON_LAYOUT in self.resource_dict:
            for resource in self.resource_dict[ResourceType.JSON_LAYOUT].get_all_resources():
                resource.get_metadata().subscribe(self.json_callback, "json")
                
    def json_callback(self, json: ResourceWrapper) -> None:
        """Callback to process image"""
        return self._process_img(json = json)
    
    def _move_items(self, path:str) -> list:
        """Move ready items into temp directory"""
        if not os.path.exists(path):
            os.makedirs(path)
            os.makedirs(os.path.join(path, 'images'))
            os.makedirs(os.path.join(path, 'annotations'))
        item_ready = []
        for val in self.img_lst.values():
            if not val["is_completed"] and val["ready"]:
                item_metadata = val["item"].get_metadata()
                shutil.copy(item_metadata.get_jpeg_path(), os.path.join(path, 'images', item_metadata.get_img_name() + ".jpeg"))
                shutil.copy(item_metadata.get_json_path(), os.path.join(path, 'annotations', item_metadata.get_img_name() + ".json"))
                item_ready.append(val["item"])
        return item_ready
            
    def _run(self) -> None:
        """Run tappable on temp batch"""
        if not self.running:
            self.running = True
            path = os.path.join(self.output_dir + "temp_dir")
            item_lst = self._move_items(path)
            #run tappable
            subprocess.call(['python3','PATH TO TAPPABLE', '-i', os.path.join(path, 'images'), '-x', os.path.join(path, 'annotations'), '-o', self.output_dir, '-t', str(self.threshold)])
            #publish
            self._publish(item_lst, path)
    
    def _publish(self, item_lst: list, path: str) -> None:
        """publishes and updates item"""
        for item in item_lst:
            #set item as complete 
            self.img_lst[item.get_path()]["is_completed"] = True
            item_metadata = item.get_metadata()
            item_metadata.set_tappability_prediction(True)
            #add new tappability prediction resources
            resource = ResourceWrapper(os.path.join(path, item_metadata.get_img_name()), item.get_origin(), item_metadata)
            for item in self.get_output_types(cls):
                if item in self.resource_dict:
                    rg = self.resource_dict[item]
                    rg.publish(resource, False)
                else:
                    rg = ResourceGroup(item)
                    rg.publish(resource, False)
        #clear temp folder
        shutil.rmtree(os.path.join(path, 'images'))
        shutil.rmtree(os.path.join(path, 'annotations'))
        os.makedirs(os.path.join(path, 'images'))
        os.makedirs(os.path.join(path, 'annotations'))
        #set tappability as not running
        self.running = False
                    
    def is_complete(self):
        """Checks if all images in list have been convertered"""
        if self._get_next() == None:
            return True
        else:
            return False  
    
        
if __name__ == '__main__':
    # make resource groups
    tappability_resource = ResourceGroup(ResourceType.TAPPABILITY_PREDICT)
    jpeg_resources = ResourceGroup[Screenshot](ResourceType.SCREENSHOT_JPEG)
    json_resources = ResourceGroup[Screenshot](ResourceType.JSON_LAYOUT)
    resource_dict = {} # make resource dict
    resource_dict[ResourceType.TAPPABILITY_PREDICT] = tappability_resource
    resource_dict[ResourceType.SCREENSHOT_JPEG] = jpeg_resources
    resource_dict[ResourceType.JSON_LAYOUT] = json_resources
    tappability = Tappability('/Users/em.ily/Desktop/xbot/', resource_dict, 50)
    
    screenshot_item = Screenshot('a2dp.Vol_.main','a2dp.Vol_.main',jpeg_path='/Users/em.ily/Desktop/xbot/a2dp.Vol.main.jpeg', json_path='/Users/em.ily/Desktop/xbot/a2dp.Vol.main.json')
    
    jpeg = ResourceWrapper('/Users/em.ily/Desktop/xbot/a2dp.Vol.main.jpeg', '', screenshot_item)
    json_item = ResourceWrapper('/Users/em.ily/Desktop/xbot/a2dp.Vol.main.json', '', screenshot_item)
    
    json_resources.publish(json_item, False)
    jpeg_resources.publish(jpeg, False)