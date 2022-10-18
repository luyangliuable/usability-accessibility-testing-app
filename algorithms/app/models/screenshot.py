from dataclasses import dataclass, field
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
    metadata: dict = field(default_factory=dict)
    
    def __init__(self, ui_screen: str, image_path: str, layout_path: str, metadata: str={}) -> None:
        self.ui_screen = ui_screen
        self.image_path = image_path
        self.layout_path = layout_path
        self.metadata = metadata
        self._set_state_id()
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
        
        tempdir = os.path.join(os.path.dirname(self.layout_path), 'temp')
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        converter = LayoutConverter(tempdir, self.layout_path, os.path.splitext(os.path.basename(self.layout_path))[0])
        return converter.execute()
    
    
    def _set_structure_id(self) -> None:
        """Generates hash from layout of screenshot"""
        if self.layout_path is None or not os.path.exists(self.layout_path):
            self.structure_id = None
        
        if self.layout_path[-4:] == '.xml':
            self.structure_id = xmlToHash(self.layout_path).get_xml_hash()
            return
        
        if self.layout_path[-5:] == '.json':
            self.structure_id = jsonToHash(self.layout_path).get_json_hash()
            return


    def _set_state_id(self, ui_screen: str, views: dict) -> str:
        view_signatures = set()
        for view in views:
            view_signature = self.get_view_signature(view)
            if view_signature is not None:
                view_signatures.add(view_signature)
        
        string = "%s{%s}" % (ui_screen, ",".join(sorted(view_signatures)))
        return hashlib.md5(string.encode('utf-8')).hexdigest()
    
        
    def _get_view_signature(self, view: dict) -> str:
        if 'visible' in view and not view['visible']:
            return
            
        view_dict = {}
        for key in ('class', 'resource_id', 'text'):
            view_dict[key] = view[key] if key in view else "None"
        if view_dict['text'] is None or len(view_dict['text']) > 50:
            view_dict['text'] = "None"
        for key in ('enabled', 'checked', 'selected'):
            view_dict[key] = key if key in view and view[key] else ""
            
        view_signature = "[class]%s[resource_id]%s[text]%s[%s,%s,%s]" % \
            (view_dict['class'],
            view_dict['resource_id'],
            view_dict['text'],
            view_dict['enabled'],
            view_dict['checked'],
            view_dict['selected'])
        return view_signature