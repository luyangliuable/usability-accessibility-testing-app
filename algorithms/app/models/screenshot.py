from dataclasses import dataclass
from PIL import Image
import os
from tasks.layout_converter import LayoutConverter
from models.xml_to_hash import *


@dataclass
class Screenshot:
    """Metadata for screenshot"""
    
    ui_screen: str
    image_path: str
    layout_path: str
    structure_id: str
    
    def __init__(self, ui_screen: str, image_path: str, layout_path: str) -> None:
        self.ui_screen = ui_screen
        self.image_path = image_path
        self.layout_path = layout_path
        self._set_structure_id()
    
    
    def get_image_jpeg(self) -> str:
        """Returns path to JPEG image of screenshot"""
        if self.image_path[-4:] == '.jpg':
            return self.image_path
        
        tempdir = os.path.join(os.path.dirname(self.image_path), 'temp')
        out_path = os.path.join(tempdir, os.path.splitext(os.path.basename(self.image_path))[0] + '.jpg')
        
        # return jpeg path if it already exists
        if os.path.exists(out_path):
            return os.path.join(out_path)
        
        # generate jpeg
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        img1 = Image.open(self.image_path)
        img1 = img1.convert('RGB')
        img1.save(out_path)
        return out_path
    
    
    def get_image_png(self) -> str:
        """Returns path to PNG image of screenshot"""
        if self.image_path[-4:] == '.png':
            return self.image_path
        
        tempdir = os.path.join(os.path.dirname(self.image_path), 'temp')
        out_path = os.path.join(tempdir, os.path.splitext(os.path.basename(self.image_path))[0] + '.png')
        
        # return png path if it already exists
        if os.path.exists(out_path):
            return out_path
        
        # generate png
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        img1 = Image.open(self.image_path)
        img1 = img1.convert('RGB')
        img1.save(out_path)
        return out_path
    
    def get_layout_json(self) -> str:
        """Returns path to layout file as JSON"""
        if self.layout_path[-5:] == '.json':
            return self.layout_path
        
        tempdir = os.path.join(os.path.dirname(self.layout_path)), 'temp'
        if not os.path.exists(tempdir):
            os.makedir(tempdir)
        converter = LayoutConverter(tempdir, self.layout_path, os.path.splitext(os.path.basename(self.layout_path))[0])
        return converter.execute()
    
    def _set_structure_id(self) -> None:
        """Generates hash from layout of screenshot"""
        if self.layout_path[-4:] == '.xml':
            self.structure_id = xmlToHash(self.layout_path).get_xml_hash()
            return
        
        if self.layout_path[-5:] == '.json':
            self.structure_id = jsonToHash(self.layout_path).get_json_hash()
            return

