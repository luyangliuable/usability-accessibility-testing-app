import os
import sys
import shutil
import re
import PIL
import tempfile
from PIL import Image
import subprocess

from event_to_screen_matcher import *
from artifact_img_converter import *
from artifact_target_creator import *
from timeconverter import main as time_converter

import json

def convert_droidbot_to_gifdroid_utg():
    print("converting utg")
    utg_file = sys.argv[1]
    events_folder = sys.argv[2]
    states_folder = sys.argv[3]

    output_folder = "./output"
    subprocess.run([ "mkdir", "output"])

    ###############################################################################
    #                                 Rename file                                 #
    ###############################################################################
    droidbot_img_file_type = "jpg"
    gifdroid_img_file_type = "png"
    img_files = file_order_sorter(states_folder, droidbot_img_file_type)

    # Gifdroid file format: web-build-[\d.*-\d.\d.]T00/w.*[Android emulator]_\d.*.png

    # Replace first part of filename with web-build which is accepted by gifdroid
    print("get target files\n")
    target_files = [re.sub("^\w*-.*-.*\d", "artifacts_", each_img_file) for each_img_file in img_files]


    # rm .jpg
    target_files = [re.sub("." + droidbot_img_file_type + "\Z", "", each_img_file) for each_img_file in target_files]

    print(target_files)

    with tempfile.TemporaryDirectory() as tmp:
        tempdirname = tmp

        target_files = [
            shutil.copyfile(
                os.path.join(states_folder, img_files[i]),
                os.path.join(tempdirname, each_target_file + str(i) + "." + droidbot_img_file_type)
            ) for i, each_target_file in enumerate(target_files)
        ]

        ###############################################################################
        #                      convert all files from jpg to png                      #
        ###############################################################################
        og_img_files = file_order_sorter(tempdirname, droidbot_img_file_type )

        im1 = [ Image.open(os.path.join(tempdirname, file)) for file in file_order_sorter(tempdirname, droidbot_img_file_type )];

        im1 = [ file.save(os.path.join(output_folder, re.sub(".jpg\Z", ".png", og_img_files[i]))) for i, file in enumerate( im1 )];

    #############################################################################
    #                             Generate json file                            #
    #############################################################################
    f = open('utg.json', 'w')
    json_output = {"events": []}

    ###############################################################################
    #                                 Extract time                                #
    ###############################################################################
    time = time_converter(utg_file, events_folder)
    time_events = time['events']

    ###############################################################################
    #                                Extract object                               #
    ###############################################################################
    focused_object = find_focused_object_classname(events_folder)

    ###############################################################################
    #                               Extract Sequence                              #
    ###############################################################################
    sequence = match_state_to_event(events_folder=events_folder)

    sequence_of_events = sequence['events']

    ###############################################################################
    #                          Combine data into sequence                          #
    ###############################################################################

    for i in range(len(sequence_of_events)):
        if 'ignore' in focused_object[i] and focused_object[i]['ignore'] == True:
            pass
        else:
            d = sequence_of_events[i].copy()
            d.update(time_events[i])
            d.update(focused_object[i])

            json_output['events'].append(d)

    json.dump(json_output, f, indent=4)

    return 0


if __name__=="__main__":
    convert_droidbot_to_gifdroid_utg()
