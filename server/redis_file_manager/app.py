from flask import Blueprint, request
from redis import Redis, StrictRedis
import json
import zlib
import uuid
import random
import pickle
import os

redis_file_manager_blueprint = Blueprint("redis_file_manager", __name__)

# r = Redis.from_url(os.environ.get('REDIS_URL'))

###############################################################################
#             Strict Redis forces redise to decode byte to string             #
###############################################################################
r = StrictRedis('localhost', 6379, decode_responses=True)

def unique_id_generator():
    res = "apk_file_" + str( uuid.uuid4() )
    return res


def flush_redis_database():
    ###############################################################################
    #           WARNING: Do not run this method or all data will be lost          #
    ###############################################################################
    r.flushdb()

@redis_file_manager_blueprint.route('/redis_file_manager/result_files', methods=["GET"])
def list_all_files():
    files = r.hgetall("result_files")
    res = []

    ###############################################################################
    #                          Convert all files to json                          #
    ###############################################################################
    for file_id in files.keys():
        res.append(file_id)

    res = {"files": res}

    return json.dumps(res), 200

@redis_file_manager_blueprint.route('/redis_file_manager/result_files', methods=["GET", "POST"])
def upload_files():
    if len(request.files) > 0:
        file = request.files['file']
        pickle.dumps(file) #Serialises data to binary so we can store to redis

        ###############################################################################
        #                         Generate random key for file                        #
        ###############################################################################
        random_key = unique_id_generator()

        #Store compressed file to redis to save space
        r.hset("result_files", str( random_key ) ,zlib.compress(pickle.dumps(file)))

    return "Upload Is Online"


@redis_file_manager_blueprint.route('/redis_file_manager')
def home():
    return "Redis file manager is online"


if __name__ == "__main__":
    # r.flushdb()
    list_all_files()
    # random_key = unique_id_generator()
    # r.hset("result_files", str( random_key ) ,"test_val")
    # print("testing retrieval", r.hget("result_files", str( random_key )))
    # print(type(str(  r.hget("result_files", str( random_key ) ))))
    # print(unique_id_generator())
    # print(unique_id_generator())
    # print(unique_id_generator())
    # print(unique_id_generator())
