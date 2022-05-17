from flask import Blueprint, request
from redis import Redis
import pickle
import os

upload_blueprint = Blueprint("upload", __name__)
r = Redis.from_url(os.environ.get('REDIS_URL'))

@upload_blueprint.route('/upload', methods=["GET", "POST"])
def upload():
    if len(request.form) > 0:
        file = request.files.get('file')
        pickle.dumps(file) #Serialises data to binary so we can store to redis

        #Store compressed file to redis to save space
        r.set("apk_file", zlib.compress(pickle.dumps(df)))

    return "Upload Is Online"
