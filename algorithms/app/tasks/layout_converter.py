import re
import json
import xmltodict
import os
from resources.resource import *
from tasks.task import Task
from typing import Callable, List


class LayoutConverter(Task):
    """Converts Xbot algorithm xml to json"""
    
    def __init__(self, output_dir, dict):
        super().__init__(output_dir, dict)
        self.xml_lst = {}
        input_type = self.get_input_types(cls)[0]
        self._sub_to_input_types(input_type, self.xml_callback)

    @classmethod
    def get_name(cls) -> str:
        return LayoutConverter.__name__

    @classmethod
    def get_input_types(cls) -> List[ResourceType]:
        return [ResourceType.XML_LAYOUT]

    @classmethod
    def get_output_types(cls) -> List[ResourceType]:
        return [ResourceType.JSON_LAYOUT]


    
    def _sub_to_input_types(self, input_type: ResourceType, callback_func: Callable) -> None:
        """Get notified when new xml is added"""
        if input_type in self.resource_dict:
                self.resource_dict[input_type].subscribe(callback_func) 
                
    def xml_callback(self, new_xml: ResourceWrapper) -> None:
         """Callback method to add xml and run converter method"""
         if new_xml.get_path() not in self.xml_lst:
             self._add_xml(new_xml)
             self.process_xml()

    def _add_xml(self, xml: ResourceWrapper) -> None:
        """Add xml to xml list"""
        xml_path = xml.get_path()
        if xml_path not in self.xml_lst:
            self.xml_lst[xml_path] = {"item": xml, "is_completed": False}
            
    def _get_next(self) -> ResourceWrapper:
        """Get next xml from list which is uncompleted"""
        xml_lst = [val["item"] for val in self.xml_lst.values() if not val["is_completed"]]
        return xml_lst[0] if len(xml_lst) > 0 else None

    def process_xml(self) -> None:
        """Process xml and update completion"""
        next_xml = self._get_next()
        self._run(next_xml)
        self.xml_lst[next_xml.get_path()]["is_completed"] = True # set complete
        
    def _run(self, item: ResourceWrapper) -> None:
        """Converts xml to json and publishes new resource wrapper"""
        #convert xml to json
        path = item.get_path()
        item_metadata = item.get_metadata()
        out_path = os.path.join(self.output_dir, item_metadata.get_img_name() + ".json")
        self._convert_xml_to_json(path, out_path)

        #add json path to metadata
        item_metadata.set_json_path(out_path)

        #add new resource wrapper
        resource = ResourceWrapper(out_path, item.get_origin(), item_metadata)
        for item in self.get_output_types(cls):
            if item in self.resource_dict:
                rg = self.resource_dict[item]
                rg.publish(resource, False)
            else:
                rg = ResourceGroup(item)
                rg.publish(resource, False)
                
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
                    focused = bool(child.pop("focused"))
                    child["visible"] = focused
                elif key =="password":
                    pw = bool(child.pop("password"))
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
                    lc = bool(child.pop("long-clickable"))
                    child["long_clickable"] = lc
                elif val == "true" or val == "false":
                    child[key] = bool(val)
                elif val == "":
                    child[key] = None
        return child

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

    def _convert_xml_to_json(self, xml_path: str, json_path: str) -> None:
        """Converts storydistiller xml file to json format"""
        with open(xml_path) as xml_file:
            data_dict = xmltodict.parse(xml_file.read(),attr_prefix='')
            data_node = data_dict["hierarchy"]["node"]

        json_file_updated= self._update_dict(data_node)

        final = []
        counter = 0
        json_node_out, _= self._node_list(json_file_updated, final, counter)

        views_out = {"views": json_node_out}

        json_str = json.dumps(views_out, indent=4)

        json_out = open(json_path, "w+")
        json_out.write(json_str)
        json_out.close()

    def is_complete(self) -> bool:
        """Checks if all xml in list have been convertered"""
        if self._get_next() == None:
            return True
        else:
            return False  
        
if __name__ == '__main__':
    # make resource groups
    xml_resource = ResourceGroup(ResourceType.XML_LAYOUT)
    resource_dict = {} # make resource dict
    resource_dict[ResourceType.XML_LAYOUT] = xml_resource
    layout_converter = LayoutConverter('/Users/em.ily/Desktop/temp/img_converter', resource_dict)
    
    xml = ResourceWrapper('/Users/em.ily/Desktop/xbot/a2dp.Vol.main.xml', '', Screenshot('a2dp.Vol_.main','a2dp.Vol_.main',png_path='/Users/em.ily/Desktop/temp/a2dp.Vol_.main.png', xml_path='/Users/em.ily/Desktop/xbot/a2dp.Vol.main.xml'))
    
    xml_resource.publish(xml, False)
    print(layout_converter.is_complete())