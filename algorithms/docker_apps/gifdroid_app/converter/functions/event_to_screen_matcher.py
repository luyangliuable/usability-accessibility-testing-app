from pickle import encode_long
from converter.functions.artifact_img_converter import *
import json


def match_state_to_event(events_folder: str):
    file_type = "json"

    event_files = file_order_sorter(events_folder, file_type)

    # print(os.path.join(events_folder, event_files[0] ))

    ###############################################################################
    #                    Load start states in sequential order                    #
    ###############################################################################
    start_states = [ json.load(open(os.path.join(events_folder, event_file )))['start_state'] for event_file in event_files]

    ###############################################################################
    #                    Load stop states in sequential order                     #
    ###############################################################################
    stop_states = [ json.load(open(os.path.join(events_folder, event_file )))['stop_state'] for event_file in event_files]


    ###############################################################################
    #                     Create lookup table for state to id                     #
    ###############################################################################

    lookup = {}
    current_id = 0

    both_states = start_states + stop_states

    for each_state in both_states:
        if each_state not in lookup:
            lookup[ each_state ] = current_id
            current_id += 1

    with open("lookup.json", "w") as f:
        json.dump(lookup, f);


    ############################################################################
    #                        Create node for each event                        #
    ############################################################################

    output = {'events': []}

    for i, event in enumerate( event_files ):
        with open(os.path.join(events_folder, event)) as f:
            data = json.load(f)
            source_screen_id = lookup[ data['start_state'] ]
            destination_screen_id = lookup[ data['stop_state'] ]

            output['events'].append({
                'sequence': i,
                'sourceScreenId': str( source_screen_id ),
                'destinationScreenId': str(destination_screen_id)
            })

    return output




if __name__ == "__main__":
    match_state_to_event("/Users/blackfish/Documents/FIT3170_Usability_Accessibility_Testing_App/docker_apps/gifdroid/converter/functions/states/", "/Users/blackfish/Documents/FIT3170_Usability_Accessibility_Testing_App/docker_apps/gifdroid/converter/functions/events/")
