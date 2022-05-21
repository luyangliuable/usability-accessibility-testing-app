import sys
from flask import Flask, request
from redis import StrictRedis
if __name__ == "__main__":
    ###############################################################################
    #            In order to make import works, must run in root folder           #
    ###############################################################################
    sys.path.append("/Users/rubber/Documents/FIT3170_Usability_Accessibility_Testing_App/StoryDistiller-main")

from storydistiller_main.code.run_storydistiller import run_everything, getSootOutput, parse, get_acy_not_launched, get_act_not_in_atg, copy_search_file, get_atgs

r = StrictRedis('localhost', 6379, decode_responses=True)
app = Flask(__name__)

@app.route('/')
def home():
    return "Story distiller app is live."

@app.route("/send_uid", methods=["POST"])
def send_uid_and_signal_run():
    if request.method == "POST":
        uid = request.get("uid")
        r.hget(str( uid ), "apk_file")

    return "No HTTP POST method received for send_uid"


def run_story_distiller():
    run_everything()

get_atgs
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=3000)
