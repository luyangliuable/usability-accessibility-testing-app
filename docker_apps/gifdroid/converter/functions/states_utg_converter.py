import json
import os
from os import listdir
from os.path import isfile, join

#Return time screen was generated given filename
def get_time(filename):
    return int(filename.split("_")[2].split(".")[0])

def create_screen_json():
    #Getting all the jpg files from local folder
    states_folder = os.getcwd() + "\states"
    files = [f for f in listdir(states_folder) if isfile(join(states_folder, f))]
    screen_files = []
    for i in range(len(files)):
        if files[i][-3:] == 'jpg':
            screen_files.append(files[i])

    #Sort based on time screen was generated
    screen_files.sort(key=get_time)

    #Iterate through jpg files in states and create json object
    events = []
    for i in range(len(screen_files)):
        screen = {
            "sourceScreenId": str(i),
            "destinationScreenId": str(i+1),
            "image_file_name": screen_files[i]
        }
        events.append(screen)

    events = {
        "events": events
    }
    return json.dumps(events)


if __name__ == "__main__":
    create_screen_json()