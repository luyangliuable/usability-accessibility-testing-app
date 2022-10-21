from importlib.resources import Resource
from resources.screenshot import Screenshot
from resources.resource import *
from tasks.task import Task
from typing import List, Tuple
import json

class UniqueScreenshots(Task):

    def __init__(self, output_dir, resource_dict):
        super.init(output_dir, resource_dict)

        self.jpegs = []
        self.jsons = []

        self.pairs = {} # jpeg, json format

        self._sub_to_jpegs()
        self._sub_to_jsons()


    @classmethod
    def get_name(cls) -> str:
        return UniqueScreenshots.__name__


    @classmethod
    def get_input_types(cls) -> List[ResourceType]:
        # return [ResourceType.SCREENSHOT_JPEG, ResourceType.JSON_LAYOUT]
        pass


    @classmethod
    def get_output_types(cls) -> List[ResourceType]:
        # return [ResourceType.SCREENSHOT_UNIQUEPAIR]
        pass


    
    def _sub_to_jpegs(self) -> None:
        """Get notified when an jpeg is available"""
        if ResourceType.SCREENSHOT_JPEG in self.resource_dict:
            self.resource_dict[ResourceType.SCREENSHOT_JPEG].subscribe(self.jpeg_callback)


    def _sub_to_jsons(self) -> None:
        """Get notified when an json is available"""
        if ResourceType.SCREENSHOT_JPEG in self.resource_dict:
            self.resource_dict[ResourceType.JSON_LAYOUT].subscribe(self.json_callback)



    def jpeg_callback(self, jpeg : ResourceWrapper[Screenshot]) -> None:
        """callback method to add jpeg"""
        self.jpegs.append(jpeg)
        jpeg.release()

        expected_json = jpeg.get_metadata().get_json_path()

        for json in self.jsons:
            if json.get_path() == expected_json:
                self.execute(jpeg, expected_json)
                break
        
    def json_callback(self, json : ResourceWrapper) -> None:
        """callback method to add jpeg"""
        self.json.append(json)
        json.release()

        expected_json = json.get_path()

        for jpeg in self.jpegs:
            if jpeg.get_metadata().get_json_path()== expected_json:
                self.execute(jpeg, expected_json)
                break


    def execute(self, new_jpeg : ResourceWrapper[Screenshot], new_json : ResourceWrapper):

        for (jpeg, json) in self.pairs:
            similarity = self._compare(json, new_json)
            if similarity == 100:
                return  # not unique so just exit function


        # JPEG was unique, keep track of it and disptach to SCREENSHOT_UNIQUEPAIR
        self.pairs[new_jpeg] = new_json
        
        result = ResourceWrapper[Tuple[ResourceWrapper[Screenshot], ResourceWrapper]](new_jpeg.get_path(), self.get_name(), (new_jpeg, new_json))
        self.resource_dict[ResourceType.SCREENSHOT_UNIQUEPAIR].dispatch(result, False)


    def _compare(self, json1_res : ResourceWrapper, json2_res : ResourceWrapper) -> Number:

        ## TODO load json text from resources
        try:
            json1 = json.load(json1_res.get_path())
            json2 = json.load(json2_res.get_path())

            json2_lst = []
            for i in json2['views']:
                if i['visible'] and i['resource_id']:
                    json2_lst.append(i['resource_id'])

            json1_lst = []
            for i in json1['views']:
                if i['visible'] and i['resource_id']:
                    json1_lst.append(i['resource_id'])

            json2_out = ''.join(sorted(json2_lst))
            json1_out = ''.join(sorted(json1_lst))

            return self._lcs_algo(json1_out, json2_out, len(json1_out), len(json2_out))

        except:
            return 0


    def _lcs_algo(str1, str2, s1len, s2len) -> Number:
        L = [[0 for x in range(s2len+1)] for x in range(s1len+1)]

        for i in range(s1len+1):
            for j in range(s2len+1):
                if i == 0 or j == 0:
                    L[i][j] = 0
                elif str1[i-1] == str2[j-1]:
                    L[i][j] = L[i-1][j-1] + 1
                else:
                    L[i][j] = max(L[i-1][j], L[i][j-1])

        index = L[s1len][s2len]
        return index / min(s1len, s2len) *100



