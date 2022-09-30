from utility import *
import subprocess

EMULATOR = os.environ.get( "EMULATOR" )

def _service_execute_droidbot(uuid: str, apk_path: str, output_dir: str):
    """
    This function execute droidbot algorithm responsible for getting the utg.js file.

    Parameters:
        uuid - The unique id for the current task.
    """

    ############################################################################
    #                      Run program with downloaded apk                     #
    ############################################################################
    subprocess.run([ "adb", "connect", EMULATOR])
    subprocess.run([ "droidbot", "-count", config[ "NUM_OF_EVENT" ], "-a", apk_path, "-o", os.path.join("/home/data/", uuid, "droidbot_result") ])

    ###############################################################################
    #                                Save utg file                                #
    ###############################################################################
    enforce_bucket_existance([config[ "BUCKET_NAME" ], "storydistiller-bucket", "xbot-bucket"])
