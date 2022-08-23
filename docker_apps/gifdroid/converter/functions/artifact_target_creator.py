import os
import sys
from artifact_img_converter import *
import json
import re

def find_focused_object_classname(events_folder: str=None):

    target_dir = events_folder

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

    focused_object = [{} for i in range(len(files))]

    for i in range(len(files)):

        with open(files[i], "r") as f:
            content = json.load(f)

        ###############################################################################
        #                            Get the focused object                           #
        ###############################################################################

        # NOTE: If no focused object exits this means no object is click in the current execution
        child_sequence = "0.0.1.0.3.0.0"

        if 'view' in content['event']:
            each_view = content['event']['view']
            # if each_view['focused'] == True:
            focused_object[i] = {
                "type": content["event"]["event_type"],
                "executionResult": "SUCCESS",
                "target": {
                    # "childSequence": child_sequence,
                    "type": content["event"]["event_type"],
                    "targetDetails": {
                        "className": each_view['class'],
                        "androidClassName": each_view['class'],
                        "textLabel": each_view['text'],
                        "contentDescription": each_view['content_description'],
                        "resourceName": each_view['resource_id'],
                    }
                }
            }

        else:
            if content['event']['event_type'] == 'kill_app':
                focused_object[i] = {
                    "ignore": True
                }
            elif content['event']['event_type'] == 'intent':
                focused_object[i] = {
                    "executionResult": "SUCCESS",
                    "launch": {
                        "action": re.sub("^.*\/", "", content['event']["intent"])
                    }
                }

    ###############################################################################
    #                              Create target json                             #
    ###############################################################################

    return focused_object


if __name__ == "__main__":
    find_focused_object_classname("/Users/blackfish/Documents/FIT3170_Usability_Accessibility_Testing_App/docker_apps/gifdroid/converter/functions/events/")
