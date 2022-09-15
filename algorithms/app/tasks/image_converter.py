from PIL import Image
import os
from resources.resource import *
from tasks.task import Task
from typing import Callable, List


class ImageConverter(Task):
    """Class for converting image types"""
    
    def __init__(self, output_dir, dict, jpeg = False, png = False):
        super().__init__(output_dir, dict)
        self.jpeg_type = jpeg
        self.png_type = png
        self.img_lst = {}
        input_type = self.get_input_types(cls)[0]
        self._sub_to_input_types(input_type, self.img_callback)


    @classmethod
    def get_name(cls) -> str:
        return ImageConverter.__name__

    @classmethod
    def get_input_types(cls) -> List[ResourceType]:
        # if self.jpeg_type:
        #     return [ResourceType.SCREENSHOT_PNG]
        # if self.png_type:
        #     return [ResourceType.SCREENSHOT_JPEG]
        return [ResourceType.SCREENSHOT_PNG]

    @classmethod
    def get_output_types(cls) -> List[ResourceType]:
        # if self.jpeg_type:
        #     return [ResourceType.SCREENSHOT_JPEG]
        # if self.png_type:
        #     return [ResourceType.SCREENSHOT_PNG]
        return [ResourceType.SCREENSHOT_JPEG]



    def _sub_to_input_types(self, type : ResourceType, callback_func: Callable) -> None:
        """Get notified when new jpeg/png is added"""
        if type in self.resource_dict:
                self.resource_dict[type].subscribe(callback_func) 
       
    def img_callback(self, new_img : ResourceWrapper) -> None:
        """Callback method to add image and run execute method on image"""
        if new_img.get_path() not in self.img_lst:
            self._add_img(new_img)
            self.process_image()

    def _add_img(self, new_img: ResourceWrapper) -> None:
        """Add image to image list"""
        img_path = new_img.get_path()
        if img_path not in self.img_lst:
            self.img_lst[img_path] = {"item": new_img, "is_completed": False}

    def _get_next(self) -> ResourceWrapper:
        """Get next image from list which is uncompleted"""
        img_lst = [val["item"] for val in self.img_lst.values() if not val["is_completed"]]
        return img_lst[0] if len(img_lst) > 0 else None

    def process_image(self) -> None:
        """Process image and update completion"""
        next_img = self._get_next()
        self._run(next_img)
        self.img_lst[next_img.get_path()]["is_completed"] = True # set complete
       
    def _run(self, item: ResourceWrapper):
        """Converts image from png to jpeg or jpeg to png and stores in output directory"""
        type_str = ''
        if self.jpeg_type:
            type_str = 'jpeg'
        elif self.png_type:
            type_str = 'png'
            
        #change file type
        path = item.get_path()
        item_metadata = item.get_metadata()
        img1 = Image.open(path)
        img1 = img1.convert('RGB')
        out_path = os.path.join(self.output_dir, item_metadata.get_img_name() + "." + type_str)
        img1.save(out_path)

        #update existing metadata
        if self.jpeg_type:
            item_metadata.set_jpeg_path(out_path)
        if self.png_type:
            item_metadata.set_png_path(out_path)

        resource = ResourceWrapper(out_path, item.get_origin(), item_metadata)
        for item in self.get_output_types(cls):
            if item in self.resource_dict:
                rg = self.resource_dict[item]
                rg.publish(resource, False)
            else:
                rg = ResourceGroup(item)
                rg.publish(resource, False)  
                
    def is_complete(self) -> bool:
        """Checks if all images in list have been convertered"""
        if self._get_next() == None:
            return True
        else:
            return False  


if __name__ == '__main__':

    # make resource groups
    png_resources = ResourceGroup(ResourceType.SCREENSHOT_PNG)
    jpeg_resources = ResourceGroup(ResourceType.SCREENSHOT_JPEG)
    resource_dict = {} # make resource dict
    resource_dict[ResourceType.SCREENSHOT_PNG] = png_resources
    resource_dict[ResourceType.SCREENSHOT_JPEG] = jpeg_resources
    img_converter = ImageConverter('/Users/em.ily/Desktop/temp/img_converter', resource_dict,png=False, jpeg=True)
    
    png = ResourceWrapper('/Users/em.ily/Desktop/temp/a2dp.Vol_.main.png', '', Screenshot('a2dp.Vol_.main','a2dp.Vol_.main',png_path='/Users/em.ily/Desktop/temp/a2dp.Vol_.main.png'))
    jpeg = ResourceWrapper('/Users/em.ily/Desktop/temp/droidbot/states/screen_2022-08-17_063729.jpeg', '', Screenshot('2022-08-17_063729','a2dp.Vol_.PackagesChooser','/Users/em.ily/Desktop/temp/droidbot/states/screen_2022-08-17_063729.jpeg'))
    
    png_resources.publish(png, False)
    jpeg_resources.publish(jpeg, False)