import sys
import os
from flask import Flask, request
from redis import StrictRedis, Redis
import pickle
import zlib
import shutil

if __name__ == "__main__":
    ###############################################################################
    #            In order to make import works, must run in root folder           #
    ###############################################################################
    sys.path.append("/Users/rubber/Documents/FIT3170_Usability_Accessibility_Testing_App/StoryDistiller-main")

# from storydistiller_main.code.run_storydistiller import run_everything, getSootOutput, parse, get_acy_not_launched, get_act_not_in_atg, copy_search_file, get_atgs

r = Redis('localhost', 6379)
app = Flask(__name__)

@app.route('/')
def home():
    return "Story distiller app is live."

@app.route("/send_uid", methods=["POST"])
def send_uid_and_signal_run():
    if request.method == "POST":

        target_apk_folder = "./storydistiller_main/apk_folder/"

        ###############################################################################
        #                             Get file from redis                             #
        ###############################################################################
        print(request.get_json()["uid"])

        # uid = ["uid"]
        # Dummy UID to test with for now
        # uid = 'apk_file_apk_file_c3ca34d4-e690-4b06-9f16-7cb3fce9fdee'

        ##############################################################################################
        # Assume that the redis database hash contains the file location not the actual file anymore #
        ##############################################################################################
        # file_location = r.hget(str( uid ), "apk_file")
        # file = r.get("uid")

        # TODO instead of referencing file locaiton, reference actual file from redis
        content = pickle.loads( r.get( uid ) )

        with open(os.path.join(target_apk_folder, uid + ".apk"), "wb") as f:
            f.write(content)

        # os.cmd("cp -f" + ( file_location ), )
        # shutil.copy(file_location, os.path.join( target_apk_folder, "apk_file.apk" ))

        ###############################################################################
        #                      Run the code inside storydistiller                     #
        ###############################################################################
        run_story_distiller()

        return "Sucessfully ran story distiller", 200


    return "No HTTP POST method received for send_uid"


def run_story_distiller():
    os.system("python2.7 ./storydistiller_main/code/run_storydistiller.py")

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=3000)
