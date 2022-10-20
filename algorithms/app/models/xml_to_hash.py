import json
import hashlib
import xmltodict
import re

class xmlToHash():
    """Helper function for Screenshot to generate a hash from an XML layout file"""
    
    def __init__(self, xml_path: str):
        self.xml_path = xml_path
        self.xml_hash = None
        self.convert_xml()
        
    def _read_xml(self):
        """Reads xml and returns view content"""
        f = open(self.xml_path).read()
        data_dict = xmltodict.parse(f,attr_prefix='')
        data_node = data_dict["hierarchy"]["node"]
        return data_node
    
    def _get_foreground_activity(self):
        """Gets foreground activity name in droidbot format"""
        file_name =  self.xml_path.split('/')[-1].strip('.xml')
        file_split = file_name.split('.')
        activity_name = '.'.join(file_split[:-1])
        fg_activity_name = activity_name + '/.' + file_split[-1]
        return fg_activity_name
    
    def get_xml_hash(self):
        return self.xml_hash
    
    def convert_xml(self):
        """Converts xml to hash """
        view_signatures = set()
        foreground_activity = self._get_foreground_activity()
        data = self._read_xml()
        regex = r'\'resource-id\': \'(.*?)\',[\s\S]*?class\': \'(.*?)\','
        views = re.findall(regex, str(data))
        for view in views:
            view_signature = self._get_content_free_view_signature(view)
            if view_signature:
                view_signatures.add(view_signature)
        state_str = "%s{%s}" % (foreground_activity, ",".join(sorted(view_signatures)))
        self.xml_hash =  hashlib.md5(state_str.encode('utf-8')).hexdigest()
    
    def _get_content_free_view_signature(self, view):
        """Formats signature for class and resource id"""
        content_free_signature = "[class]%s[resource_id]%s" % \
                                    (self._process_signature(view, 1),
                                    self._process_signature(view, 0))
        return content_free_signature
        
    def _process_signature(self, view, key):
        """Helper function to return value from array"""
        if len(view[key]) == 0:
            return "None"
        else:
            return view[key]
        
    def compare_hash(self, hash):
        """Compares two hashes"""
        return self.xml_hash == hash
   
   
class jsonToHash():
    """Helper function for Screenshot to generate a hash value for a screenshot UI layout"""
    
    def __init__(self, json_path):
        self.json_path = json_path
        self.xml_hash = None
        self.convert_json()
     
    def _get_content_free_view_signature_json(self, view_dict):
        """Returns class and resource id signature"""
        if 'content_free_signature' in view_dict:
                return view_dict['content_free_signature']
        content_free_signature = "[class]%s[resource_id]%s" % \
                                    (self._safe_dict_get(view_dict, 'class', "None"),
                                    self._safe_dict_get(view_dict, 'resource_id', "None"))
        view_dict['content_free_signature'] = content_free_signature
        return content_free_signature

    def _safe_dict_get(self, view_dict, key, default=None):
        """Helper function"""
        return view_dict[key] if (key in view_dict) else default
        
    def convert_json(self):
        """
        Converts json to hash
        """
        view_signatures = set()
        json_file = self._read_json()
        views = json_file['views']
        for view in views:
            view_signature = self._get_content_free_view_signature_json(view)
            if view_signature and view['visible']:
                view_signatures.add(view_signature)
        state_str = "%s{%s}" % (json_file['foreground_activity'], ",".join(sorted(view_signatures)))
        self.json_hash = hashlib.md5(state_str.encode('utf-8')).hexdigest()

    def get_json_hash(self):
        return self.json_hash
    
    def _read_json(self):
        """Reads json from path"""
        f = open(self.json_path).read()
        j = json.loads(f)
        return j
    
    def compare_hash(self, hash):
        """Compares two hashes"""
        return self.json_hash == hash


if __name__ == '__main__':
    
    xml = xmlToHash('/Users/em.ily/Desktop/temp/xbot/screenshot/layouts/a2dp.Vol.PackagesChooser.xml')
    
    j = jsonToHash()
    h2 = j.convert_json("C:/Users/trevi/OneDrive/Desktop/droidbot_test/out/states/state_2022-10-06_000150.json")
    
    print(h2)
    print(xml.compare_hash(h2))
    # print(xml.similarilty_percent(h2))
    
    