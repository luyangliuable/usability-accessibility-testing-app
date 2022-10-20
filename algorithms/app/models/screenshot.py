from dataclasses import dataclass, field
from PIL import Image
import os
import xmltodict
import json
import hashlib
import re


@dataclass
class Screenshot:
    """Metadata for screenshot"""
    
    ui_screen: str
    image_path: str
    layout_path: str
    screenshot_id: str = None
    structure_id: str = None
    state_id: str = None
    metadata: dict = field(default_factory=dict)
    
    def __init__(self, ui_screen: str, image_path: str, layout_path: str=None, metadata: dict={}) -> None:
        self.ui_screen = ui_screen
        self.image_path = image_path
        self.layout_path = layout_path
        self.metadata = metadata
        if layout_path:
            _hash = LayoutHash(self.get_layout_path(file_type='json'), ui_screen)
            self.screenshot_id = _hash.get_screenshot_id()
            self.structure_id = _hash.get_structure_id()
            self.state_id = _hash.get_state_id()
        
    
    def get_image_path(self, file_type: str=None) -> str:
        """Returns path to image of screenshot.
        
        Args:
            file type: 'jpg' or 'png'
            
        Returns:
            Absolute path to image file for specified file type.
            Original path is returned if file type not specified. 
        """
        if not file_type or self.image_path.split('.')[-1] == file_type:
            return self.image_path
        
        tempdir = os.path.join(os.path.dirname(self.image_path), 'temp')
        out_path = os.path.join(tempdir, os.path.splitext(os.path.basename(self.image_path))[0] + f'.{file_type}')
        print(out_path)
        # return temp image path if it already exists
        if os.path.exists(out_path):
            return os.path.join(out_path)
        
        # convert image
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        img1 = Image.open(self.image_path)
        img1 = img1.convert('RGB')
        img1.save(out_path)
        return out_path
    
    def get_layout_path(self, file_type: str=None) -> str:
        """Returns path to screenshot layout file.
        
        Args:
            file type: 'xml' or 'json'
            
        Returns:
            Absolute path to layout file for specified file type.
            Original path is returned if file type not specified. 
        """
        cur_type = self.layout_path.split('.')[-1]
        if not file_type or cur_type == file_type:
            return self.layout_path
        
        tempdir = os.path.join(os.path.dirname(self.layout_path), 'temp')
        filename = f'{os.path.basename(self.layout_path)[0]}.{file_type}'
        if os.path.exists(os.path.join(tempdir, filename)):
            return os.path.join(tempdir, filename)
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        
        if cur_type == 'xml' and file_type == 'json':
            converter = LayoutConverter(self.layout_path, self.ui_screen)
            json_path = os.path.join(tempdir, f'{filename}.json')
            converter(output_path=json_path)
            return json_path    

    

class LayoutConverter():
    """Converts Xbot algorithm xml to json"""
    
    def __init__(self, layout_path, activity_name):
        self.activity_name = activity_name
        self.xml_path = layout_path
    
    def __call__(self, output_path=None) -> str:
        """Converts xml to json and publishes new resource wrapper"""
        #convert xml to json

        with open(self.xml_path) as xml_file:
            data_dict = xmltodict.parse(xml_file.read(),attr_prefix='')
            data_node = data_dict["hierarchy"]["node"]

        json_file_updated= self._update_dict(data_node)

        final = []
        counter = 0
        json_node_out, _= self._node_list(json_file_updated, final, counter)

        views_out = {"views": json_node_out}
        

        if output_path:
            json_str = json.dumps(views_out, indent=4)
            if not os.path.exists(output_path):
                json_out = open(output_path, "w+")
                json_out.write(json_str)
                json_out.close()
            
        return views_out
                
    def _update_list(self, json_children: list) -> list:
        """Loops through list of children and calls update on individual dictionary"""
        out = []
        for child in json_children:
            child_out = self._update_dict(child)
            out.append(child_out)
        return out

    def _update_dict(self, child: dict) -> dict:
        """Updates json file for dictionary item and children. Renames keys, change type of values and format null"""
        if "node" not in child:
            child["child_count"] = 0
        children_copy = child.copy()
        for key, val in children_copy.items():
                if key == 'index':
                    child[key] = int(val)
                elif key == "node":
                    child["children"] = child.pop("node")
                    if type(child["children"]) == list:
                        child["child_count"] = len(child["children"])
                    else:
                        child["child_count"] = 1
                    if child["child_count"] > 1:
                        child["children"] = self._update_list(child["children"])
                    else:
                        child["children"] = self._update_dict(child["children"])
                elif key =="bounds":
                    re_text = r"\[(\d*?),(\d*?)\]\[(\d*?),(\d*?)\]"
                    bounds_out = re.findall(re_text, val)[0]
                    bounds_json = [[int(bounds_out[0]), int(bounds_out[1])], [int(bounds_out[2]), int(bounds_out[3])]]
                    child[key] = bounds_json
                elif key == "focused":
                    focused = self._get_bool(child.pop("focused"))
                    child["focused"] = focused
                elif key =="password":
                    pw = self._get_bool(child.pop("password"))
                    child["is_password"] = pw
                elif key =="resource-id":
                    ri = child.pop("resource-id")
                    if ri =="":
                        ri = None
                    child["resource_id"] = ri
                elif key =="content-desc":
                    cd = child.pop("content-desc")
                    if cd =="":
                        cd = None
                    child["content_description"] = cd
                elif key =="long-clickable":
                    lc = self._get_bool(child.pop("long-clickable"))
                    child["long_clickable"] = lc
                elif val == "true" or val == "false":
                    child[key] = self._get_bool(val)
                elif val == "":
                    child[key] = None
        return child
    
    def _get_bool(self, val: str) -> bool:
        return False if val.lower() == 'false' else True

    def _node_list(self, a: list, final: list, counter: int) -> list:
        """Converts node heiarachy to node list"""
        if "children" in a:
            out = []
            if type(a["children"])==list:
                for child in a["children"]:
                    final, counter= self._node_list(child.copy(), final.copy(), counter)
                    out.append(counter)
                    counter +=1
            else:
                final, counter= self._node_list(a["children"].copy(), final.copy(), counter)
                out.append(counter)
                counter +=1
            a["children"] = out.copy()
        final.append(a.copy())
        return final, counter


class LayoutHash():
    """Helper function for Screenshot to generate a hash value for a screenshot UI layout"""
    _view_filters = [
            ('visible', False),
            ('resource_id', 'android:id/navigationBarBackground'),
            ('resource_id', 'android:id/statusBarBackground')
        ]
    
    def __init__(self, json_path: str, activity_name: str):
        self.json_path = json_path
        self.activity_name = activity_name
        self.views = None
        self._get_views()
        
    def get_screenshot_id(self):
        view_signatures = set()
        for view in self.views:
            view_signature = self._get_view_signature(view, filter_views=True)
            if view_signature:
                view_signatures.add(view_signature)
        state_str = "%s{%s}" % (self.activity_name, ",".join(sorted(view_signatures)))
        return hashlib.md5(state_str.encode('utf-8')).hexdigest()
    
    def get_state_id(self) -> str:
        view_signatures = set()
        for view in self.views:
            view_signature = self._get_view_signature(view)
            if view_signature:
                view_signatures.add(view_signature)
        state_str = "%s{%s}" % (self.activity_name, ",".join(sorted(view_signatures)))
        return hashlib.md5(state_str.encode('utf-8')).hexdigest()
    
    def get_structure_id(self) -> str:
        """
        Converts json to hash
        """
        view_signatures = set()
        for view in self.views:
            view_signature = self._get_content_free_view_signature_json(view)
            if view_signature:
                view_signatures.add(view_signature)
        structure_str = "%s{%s}" % (self.activity_name, ",".join(sorted(view_signatures)))
        return hashlib.md5(structure_str.encode('utf-8')).hexdigest()
    
    def _get_views(self) -> list:
        """Reads json from path"""
        if not self.views:
            with open(self.json_path) as f:
                layout = json.loads(f.read())
                self.views = layout['views']
        return self.views
         
    def _get_view_signature(self, view_dict: dict, filter_views=False) -> str:
        
        if filter_views:
            for item in LayoutHash._view_filters:
                if item[0] in view_dict and view_dict[item[0]] == item[1]:
                    return
        
        for key in ('class', 'resource_id', 'text'):
            view_dict[key] = self._safe_dict_get(view_dict, key, 'None')
        if view_dict['text'] is None or len(view_dict['text']) > 50:
            view_dict['text'] = 'None'
        for key in ('enabled', 'checked', 'selected'):
            view_dict[key] = self._key_if_true(view_dict, key)
        
        view_signature = "[class]%s[resource_id]%s[text]%s[%s,%s,%s]" % \
            (
                view_dict['class'],
                view_dict['resource_id'],
                view_dict['text'],
                view_dict['enabled'],
                view_dict['checked'],
                view_dict['selected']
            )
        return view_signature
        
    def _get_content_free_view_signature_json(self, view_dict: list):
        """Returns class and resource id signature"""
        filter_dict = [
            ('visible', False),
            ('resource_id', 'android:id/navigationBarBackground'),
            ('resource_id', 'android:id/statusBarBackground')
        ]
        for item in filter_dict:
            if item[0] in view_dict and view_dict[item[0]] == item[1]:
                return
        content_free_signature = "[class]%s[resource_id]%s" % \
                                    (self._safe_dict_get(view_dict, 'class', "None"),
                                    self._safe_dict_get(view_dict, 'resource_id', "None"))
        return content_free_signature
    
    def _safe_dict_get(self, view_dict, key, default=None):
        """Helper function"""
        return view_dict[key] if (key in view_dict) else default
    
    def _key_if_true(self, view_dict, key):
        return key if (key in view_dict and view_dict[key]) else ""
    
    def compare_hash(self, hash):
        """Compares two hashes"""
        return self.get_state_id() == hash