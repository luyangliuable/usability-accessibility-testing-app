import json
import hashlib
import xmltodict
import re

#views in droidbot only 
ADD_LST = ['[class]android.view.View[resource_id]android:id/statusBarBackground', '[class]android.view.View[resource_id]android:id/navigationBarBackground']

class xmlToHash():
    """Converts XML to Layout Hash"""
    
    def __init__(self, xml_path: str):
        self.xml_path = xml_path
        self.xml_hash = None
        self.view_lst = None
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
        for item in ADD_LST:
            view_signatures.add(item)
        state_str = "%s{%s}" % (foreground_activity, ",".join(sorted(view_signatures)))
        self.xml_hash =  hashlib.md5(state_str.encode('utf-8')).hexdigest()
        # self.view_lst = view_signatures --uncomment for percent similarity
    
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
    
    def similarilty_percent(self, view_lst):
        """Similarity percent of two lists"""
        count = 0 
        if len(self.view_lst) < len(view_lst):
            lst1 = self.view_lst
            lst2 = view_lst
        else:
            lst1 = view_lst
            lst2 = self.view_lst
        for i in lst1:
            if i in lst2:
                count +=1
        return count / len(lst1) * 100
    
   
   
class jsonToHash():
    
    def __init__(self):
        pass
     
    def get_content_free_view_signature_json(self, view_dict):
        if 'content_free_signature' in view_dict:
                return view_dict['content_free_signature']
        content_free_signature = "[class]%s[resource_id]%s" % \
                                    (self.safe_dict_get(view_dict, 'class', "None"),
                                    self.safe_dict_get(view_dict, 'resource_id', "None"))
        view_dict['content_free_signature'] = content_free_signature
        return content_free_signature

    def safe_dict_get(view_dict, key, default=None):
        return view_dict[key] if (key in view_dict) else default

    def process_signature(view, key):
        if len(view[key]) == 0:
            return "None"
        else:
            return view[key]
        
    def convert_json(self, json_path):
        """
        Converts 
        """
        view_signatures = set()
        json_file = self.read_json(json_path)
        views = json_file['views']
        for view in views:
            view_signature = self.get_content_free_view_signature_json(view)
            if view_signature:
                view_signatures.add(view_signature)
        # return view_signatures --uncomment for percent similarity
        state_str = "%s{%s}" % (json_file['foreground_activity'], ",".join(sorted(view_signatures)))
        return hashlib.md5(state_str.encode('utf-8')).hexdigest()

    def read_json(self, json_path):
        f = open(json_path).read()
        j = json.loads(f)
        return j


if __name__ == '__main__':
    
    xml = xmlToHash('/Users/em.ily/Desktop/temp/xbot/screenshot/layouts/a2dp.Vol.PackagesChooser.xml')
    
    j = jsonToHash()
    h2 = j.convert_json('/Users/em.ily/Desktop/temp/droidbot/states/state_2022-08-17_063729.json')
    
    print(xml.compare_hash(h2))
    # print(xml.similarilty_percent(h2))
    
    