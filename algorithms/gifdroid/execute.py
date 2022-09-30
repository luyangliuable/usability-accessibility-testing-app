from utility import *
import subprocess
from run import *

EMULATOR = os.environ.get( "EMULATOR" )

def _service_execute_gifdroid(uuid: str, droidbot_result_folder: str, gif_file_path: str, output_dir: str) -> bool:
    ###############################################################################
    #                        Convert utg to correct format                        #
    ###############################################################################
    utg = os.path.join(droidbot_result_folder, config['DEFAULT_UTG_FILENAME'])
    events = os.path.join(droidbot_result_folder, "events" )
    states = os.path.join(droidbot_result_folder, "states")

    new_converted_utg = convert_droidbot_to_gifdroid_utg(utg, events, states, output_dir=output_dir)

    subprocess.run([ "python3", "main.py", f'--video=./{gif_file_path}', f'--utg={new_converted_utg}', f'--artifact={output_dir}', f'--out={output_dir}'])

    return True

def gifdroid_execute_cmd(gif_file_path: str, output_dir):
    pass
