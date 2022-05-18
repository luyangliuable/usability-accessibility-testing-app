from flask import Blueprint, request
from redis import Redis
import uuid
import random
import pickle
import os

upload_blueprint = Blueprint("upload", __name__)
# r = Redis.from_url(os.environ.get('REDIS_URL'))

def unique_id_generator():
    res = "apk_file_" + str( uuid.uuid4() )
    return res

@upload_blueprint.route('/upload', methods=["GET", "POST"])
def upload():
    if len(request.form) > 0:
        file = request.files.get('file')
        pickle.dumps(file) #Serialises data to binary so we can store to redis

        #Store compressed file to redis to save space
        r.set("apk_file", zlib.compress(pickle.dumps(df)))

    return "Upload Is Online"

if __name__ == "__main__":
    print(unique_id_generator())
    print(unique_id_generator())
    print(unique_id_generator())
    print(unique_id_generator())
