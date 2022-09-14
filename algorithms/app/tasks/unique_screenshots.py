from resources.resource import ResourceGroup, ResourceWrapper
from resources.resource import ResourceType
from tasks.task import Task
from typing import List

class UniqueScreenshots(Task):

    def __init__(self, output_dir, resource_dict):
        super.init(output_dir, resource_dict)


    @classmethod
    def get_name() -> str:
        return UniqueScreenshots.__name__


    @classmethod
    def get_input_types(self) -> List[ResourceType]:
        return [ResourceType.SCREENSHOT_JPEG]


    @classmethod
    def get_output_types(self) -> List[ResourceType]:
        return [ResourceType.SCREENSHOT_UNIQUE]


    def execute(self):
        #get existing unique images
        output_type = self.get_output_types()[0]
        if output_type not in self.resource_dict:
            ResourceGroup(self.get_output_types(), None)

        for type in self.get_input_types():
            unique_img_lst = self.dict[output_type].get_all_resources()
            item_lst = self.dict[type].get_all_resources()

            for item in item_lst:
                item_metadata = item.get_metadata()
                if item_metadata.get_json_path == "":
                    #subscribe to screenshot if no json
                    item_metadata.subscribe()
                else:
                    #compare item json against existing unique json
                    json1 = item_metadata.get_json_path()
                    unique = True
                    for unique_item in unique_img_lst:
                        unique_item_metadata = unique_item.get_metadata()
                        json2 = unique_item_metadata.get_json_path()
                        similarity = self._compare(json1, json2)
                        if similarity == 100:
                            unique = False
                    #add to resource if unique
                    if unique:
                        resource = ResourceWrapper(self.output_dir, item.get_origin(), item.get_metadata())
                        rg = self.resource_dict[output_type]
                        rg.dispatch(resource, False)


    def _compare(self, json1, json2) -> None:
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


    def _lcs_algo(str1, str2, s1len, s2len):
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



