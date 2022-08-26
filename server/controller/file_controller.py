from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import datetime
import json
import uuid
from models.Apk import ApkManager

###############################################################################
#                            Set Up Flask Blueprint                           #
###############################################################################
file_blueprint = Blueprint("file", __name__)

###############################################################################
#                                    Schema                                   #
###############################################################################
data = {
    "uuid": None,
    "date": str( datetime.datetime.now() ),
    "apk": [],
    "additional_files": [],
    "tapshoe_files": [],
    "storydistiller_files": [],
    "gifdroid_files": [],
    "utg_files": [],
    "owleye_files": [],
    "venus_files": [],
}

###############################################################################
#                          Initiate database instance                         #
###############################################################################
mongo = ApkManager.instance()


@file_blueprint.route("/file", methods=['GET'])
@cross_origin()
def check_health():
    """
    Method file controller files and submiting CRUD/REST API requests into
    """

    return "Working", 200


@file_blueprint.route("/file/get", methods=['GET'])
@cross_origin()
def get_document():
    """
    Method for getting a document from api
    """
    print("Starting get document")
    if request.method == "GET":
        uuid = request.json['uuid']
        result = mongo.get_document(uuid=uuid)

        result = [item for item in result]

        ###############################################################################
        #                  TODO can't serialised some parts of result                 #
        ###############################################################################

        return safe_serialize(result), 200

    return "Invalid request", 400


@file_blueprint.route("/file/add", methods=['GET', "POST"])
@cross_origin()
def add_documment():
    ###############################################################################
    #                  TODO add method for adding new document in                 #
    ###############################################################################
    if request.method == "POST":

        collection = "apk"
        document = data

        for each_key, _ in document.items():
            document[each_key] = request.args.get(each_key)

        document['uuid'] = unique_id_generator()
        print(document)

        post_id = mongo.insert_document(document, mongo.get_collection('apk')).inserted_id

        return document['uuid'], 200

    return "Not a valid request", 400

###############################################################################
#                    TODO Add file for updating a document                    #
###############################################################################

###############################################################################
#                  TODO add method file getting one document                  #
###############################################################################


###############################################################################
#                              Utility Functions                              #
###############################################################################
def safe_serialize(obj):
  default = lambda o: f"<<non-serializable: {type(o).__qualname__}>>"
  return json.dumps(obj, default=default)


def unique_id_generator():
    res = str( uuid.uuid4() )
    return res


if __name__ == "__main__":
    pass
