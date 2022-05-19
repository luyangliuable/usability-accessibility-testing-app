from flask import Blueprint, request
from redis import Redis, StrictRedis
import warnings
import codecs
import json
import zlib
import uuid
import pickle
import os

upload_blueprint = Blueprint("upload", __name__)
# r = Redis.from_url(os.environ.get('REDIS_URL'))
r = StrictRedis(decode_responses=True)

def unique_id_generator():
    res = "apk_file_" + str( uuid.uuid4() )
    return res


@upload_blueprint.route('/upload/apk', methods=["GET"])
def check_uploaded_apk_files():
    """
    This blueprint method acts as an api file uploader. It must be uploaded using form-data.
    The key in json for the apk file must be apk_file.
    """
    print("form", request.form)


    if request.method == "GET":
        redis_result = r.keys("apk_file*")
        print(redis_result)

        return json.dumps({"uploaded_apk_files": redis_result } ), 200

    return "no valid http request received", 200


@upload_blueprint.route('/upload/apk', methods=["POST"])
def upload():
    """
    This blueprint method acts as an api file uploader. It must be uploaded using form-data.
    The key in json for the apk file must be apk_file.
    """
    if request.method == "POST":
        ###############################################################################
        #                        If post http request received                        #
        ###############################################################################
        file = request.form.get('apk_file', "no file")
        if file == "no file":
            warnings.warn("No file is detected in POST request.")

        ###############################################################################
        #                              Generate unique id                             #
        ###############################################################################
        file_key = "apk_file_" + unique_id_generator()

        ###############################################################################
        #                   Compress and byte serialise the apk file                  #
        ###############################################################################
        r.set(file_key, zlib.compress(pickle.dumps(file)))
        # r.set(file_key, file)

        return json.dumps({"file_key": str( file_key ) } ), 200


    return "no request file received", 200

@upload_blueprint.route('/upload/apk')
def home():
    return "Upload Is Online"

if __name__ == "__main__":
    print(unique_id_generator())
    print(unique_id_generator())
    print(unique_id_generator())
    print(unique_id_generator())
