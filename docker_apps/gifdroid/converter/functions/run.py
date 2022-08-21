import os
import sys
import shutil
import re
# from PIL import image
import subprocess

from artifact_img_converter import *
from artifact_target_creator import *
from timeconverter import main as time_converter

import json

def convert_droidbot_to_gifdroid_utg():
    ###############################################################################
    #                                   Get time                                  #
    ###############################################################################

    print("converting utg")
    utg_file = sys.argv[1]
    events_folder = sys.argv[2]
    states_folder = sys.argv[3]

    output_folder = "./output"
    subprocess.run([ "mkdir", "output"])

    time = time_converter(utg_file, events_folder)

    ###############################################################################
    #                               Get target info                               #
    ###############################################################################

    focused_object = find_focused_object_classname(states_folder)

    ###############################################################################
    #                                 Rename file                                 #
    ###############################################################################
    droidbot_img_file_type = "jpg"
    gifdroid_img_file_type = "png"
    img_files = file_order_sorter(states_folder, droidbot_img_file_type)

    # Gifdroid file format: web-build-[\d.*-\d.\d.]T00/w.*[Android emulator]_\d.*.png

    # Replace first part of filename with web-build which is accepted by gifdroid
    target_files = [re.sub("^\w*_", "web-build_", each_img_file) for each_img_file in img_files]

    # rm .jpg
    target_files = [re.sub("." + droidbot_img_file_type + "\Z", "", each_img_file) for each_img_file in img_files]

    print(target_files)

    target_files = [
        shutil.copyfile(
            os.path.join(states_folder, img_files[i]),
            os.path.join(output_folder, each_target_file + "_" + str(i) + "." + droidbot_img_file_type)
        ) for i, each_target_file in enumerate(target_files)
    ]

    ###############################################################################
    #                      convert all files from jpg to png                      #
    ###############################################################################
    # im1 = [ image.open(os.path.join(output_folder, file)) for file in file_order_sorter(output_folder, droidbot_img_file_type )];

    # im1 = [ image.save(os.path.join(output_folder, re.sub(".jpg\Z", ".png", file))) for file in img1];

    #############################################################################
    #                             Generate json file                            #
    #############################################################################
    json_output = {}

    json_output['events'] = time['events']
    print(len( json_output['events'] ))

    print(json_output)
    print(focused_object)
    print(len(focused_object))

    # for i in range(len(time)):




if __name__=="__main__":
    convert_droidbot_to_gifdroid_utg()
