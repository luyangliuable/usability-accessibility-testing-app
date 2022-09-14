from os import walk
import json
import sys
from datetime import datetime

utg_template = {
    "events":[]
}
def string_inserter(orig_string, insert_string, pos):
    orig_string = orig_string[:pos]+insert_string+orig_string[pos:]
    return orig_string

def main(droidbot_utg_file: str=None, events_folder: str=None):
    # Get Initial Start Time and Total Time [1]

    utg_input = open(droidbot_utg_file)

    raw_utg_input = utg_input.read()
    json_utg_input = raw_utg_input[raw_utg_input.find('{') : raw_utg_input.rfind('}')+1]
    json_utg = json.loads(json_utg_input)

    initial_start_time = json_utg["test_date"]
    start_time_date = datetime.strptime(initial_start_time,'%Y-%m-%d %H:%M:%S')
    initial_total_time = json_utg["time_spent"]

    # Open event files and copy values
    previous_time = start_time_date
    cumulative_counter = 0

    for root, dirs, filenames in walk(events_folder):
        for events_json_file in filenames:
            utg_event_template = {
                "startTimeSeconds": 0,
                "endTimeSeconds": 0
            }
            # Extract event
            events_json = open(root+"/"+events_json_file,"r")
            json_event= json.load(events_json)

            # Format Event Time
            event_raw_time = json_event["tag"]
            event_raw_time = event_raw_time.replace("_"," ")
            event_raw_time = string_inserter(event_raw_time,":",15)
            event_raw_time = string_inserter(event_raw_time,":",13)

            # Get Total Seconds
            event_time = datetime.strptime(event_raw_time,"%Y-%m-%d %H:%M:%S")
            time_spent = (event_time-previous_time).total_seconds()

            # Update Previous time and cumulative counter and update UTG_event
            utg_event_template["startTimeSeconds"] = cumulative_counter
            previous_time = event_time
            cumulative_counter+=time_spent
            utg_event_template["endTimeSeconds"] = cumulative_counter

            # add to utg events
            utg_template["events"].append(utg_event_template)
            events_json.close()


    # print(utg_template)
    return utg_template
    # Open Final Json File and create JSON file
    # converter_output = open("gifdroidInput/utg.json","w") #TODO: change to corresponding filepath
    # # Dump json created into it
    # json.dump(utg_template,converter_output)
    # converter_output.close()
    # utg_input.close()

if __name__=="__main__":
    main()


# References
# [1] JS JSON: https://stackoverflow.com/questions/46946227/reading-json-data-from-js-file
# [2] os.walk(): https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
