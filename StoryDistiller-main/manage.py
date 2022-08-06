import sys
import os
from flask import Flask, request, jsonify
from task import celery, create_storydistiller_task
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
        ###############################################################################
        #                             Get file from redis                             #
        ###############################################################################
        print(request.get_json()["uid"])
        uid = request.get_json()["uid"]

        ###############################################################################
        #                       Start celery task for distiller                       #
        ###############################################################################

        ###############################################################################
        #                      Run the code inside storydistiller                     #
        ###############################################################################
        # task = create_storydistiller_task.delay({"uid": uid })
        task = run_story_distiller_with_celery({"uid": uid })

        return jsonify( {"task_id": task.id, "uid": str( uid )} ), 200

    return "No HTTP POST method received for send_uid"


@app.route("/status/<task_id>", methods=["GET"])
def check_story_distiller_with_celery(task_id):
    print('getting task id', task_id)

    task_result = celery.AsyncResult(task_id)

    print("task_result",task_result)

    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }

    return jsonify(result), 200


def run_story_distiller_with_celery(info):
    task = create_storydistiller_task.delay()
    return task

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5001)
