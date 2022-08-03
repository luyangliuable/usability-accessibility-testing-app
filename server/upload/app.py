from flask import Blueprint, request, jsonify, make_response
from redis import Redis, StrictRedis
from werkzeug.utils import secure_filename
# from celery.result import AsyncResult
from flask_cors import cross_origin
from werkzeug.datastructures import  FileStorage
from tasks import create_task, celery
import warnings
import linecache
import json
import codecs
import json
import zlib
import uuid
import pickle
import os

upload_blueprint = Blueprint("upload", __name__)
# r = Redis.from_url(os.environ.get('REDIS_URL'))
# r = StrictRedis(decode_responses=True)
r = Redis()

def unique_id_generator():
    res = "apk_file_" + str( uuid.uuid4() )
    return res

# @upload_blueprint.route('/upload/apk', methods=["GET"])
# def check_uploaded_apk_files():
#     """
#     This blueprint method acts as an api file uploader. It must be uploaded using form-data.
#     The key in json for the apk file must be apk_file.
#     """
#     print("form", request.form)


#     if request.method == "GET":
#         redis_result = r.keys("apk_file*")
#         print(redis_result)

#         return json.dumps({"uploaded_apk_files": redis_result } ), 200

#     return "no valid http request received", 200


@upload_blueprint.route('/upload/apk', methods=["POST"])
def upload():
    """
    This blueprint method acts as an api file uploader. It must be uploaded using form-data.
    The key in json for the apk file must be apk_file.
    """
    print("upload start...")
    # print(request.get_data())

    if request.method == "POST":
        ###############################################################################
        #                        If post http request received                        #
        ###############################################################################
        try:
            print("[0] Getting request from front-end")
            file = str( request.get_data() )

            ###############################################################################
            #                              Generate unique id                             #
            ###############################################################################

            file_key = "apk_file_" + unique_id_generator()

            ###############################################################################
            #                   Compress and byte serialise the apk file                  #
            ###############################################################################
            # r.set(file_key, zlib.compress(pickle.dumps(file)))
            print("[1] putting file into redis")
            r.set(file_key, pickle.dumps( file ))   # TODO: Throws exception 


            print("[2] creating celery task")
            task = create_task.delay()

            print("[3] return celery task id and file key")
            
            response = json.dumps({"file_key": str( file_key ), "task_id": task.id}), 200
            return response

        except:
            print("[!] failed to uploaded apk and start celery task")

            response = json.dumps({'code': 500, 'errorTypr': 'Internal Server Error', 'errorMessage': 'Failed to uploaded apk and start celery task'}), 500
            return response

    return "no request file received", 400

@upload_blueprint.route('/upload/apk')
def home():
    return "Upload Is Online"


@upload_blueprint.route("/upload/<task_id>", methods=["GET"])
def get_status(task_id):
    print('getting task id', task_id)

    task_result = celery.AsyncResult(task_id)

    print("task_result",task_result)

    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }

    return jsonify(result), 200

@upload_blueprint.after_request
def after_request(response):
    #response.headers['Access-Control-Allow-Origin'] = '*'
    #response.headers['Access-Control-Allow-Headers'] = '*'
    #response.headers['Access-Control-Allow-Methods'] = '*'

    # response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,timeout')
    # Other headers can be added here if needed
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # response.headers.add('access-control-allow-headers', 'Content-Type')
    # response.headers.add('access-control-allow-headers', 'authorization')
    # response.headers.add('Access-Control-Allow-Methods', 'POST')

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response

if __name__ == "__main__":
    print(unique_id_generator())
    print(unique_id_generator())
    print(unique_id_generator())
    print(unique_id_generator())
