import os
import sys
from artifact_img_converter import *
import json

def find_focused_object_classname():
    target_dir = sys.argv[1]
    file_type = "json"


    ###############################################################################
    #                       Get all files ranked by sequence                      #
    ###############################################################################
    sorted_json_files = file_order_sorter(target_dir, file_type)

    ###############################################################################
    #                 Get the classname out of each sequence file                 #
    ###############################################################################
    files = [os.path.join(target_dir, each_file) for each_file in sorted_json_files]
    print("Getting json file location", files)

    focused_object = [[] for i in range(len(files))]
    for i in range(len(files)):

        with open(files[i], "r") as f:
            content = json.load(f)

        # print(content['class'])
        ###############################################################################
        #                            Get the focused object                           #
        ###############################################################################

        # NOTE: If no focused object exits this means no object is click in the current execution

        focused_object[i] = [each_view['class'] for each_view in content['views'] if each_view['focused'] == True]

        # TODO How to tell?
        execution_result = "SUCCESS"

        # TODO How to tell?
        child_sequence = "0.0.1.0.3.0.0"

        ###############################################################################
        #                              Create target json                             #
        ###############################################################################

        target = [{
            "type": "TAP",
            "childSequence": child_sequence,
            "targetDetails": {
                "className": each_focused_object,
                "androidClassName": each_focused_object,
                "contentDescription": "Phone",
            }
        } for each_focused_object in focused_object]

    print(target)





# def get_child_sequence():


if __name__ == "__main__":
    find_focused_object_classname()
