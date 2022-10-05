from utility import *
import subprocess

EMULATOR = os.environ.get( "EMULATOR" )

def _service_execute_droidbot(apk_path: str, output_dir: str):
    """
    This function execute droidbot algorithm responsible for getting the utg.js file.

    Parameters:
        uuid - The unique id for the current task.
    """

    ############################################################################
    #                      Run program with downloaded apk                     #
    ############################################################################
    subprocess.run([ "adb", "connect", EMULATOR])
    print(output_dir)
    subprocess.run([ "droidbot", "-count", config[ "NUM_OF_EVENT" ], "-a", apk_path, "-o", output_dir ])

    ###############################################################################
    #                                Save utg file                                #
    ###############################################################################
    enforce_bucket_existance([config[ "BUCKET_NAME" ], "storydistiller-bucket", "xbot-bucket"])
