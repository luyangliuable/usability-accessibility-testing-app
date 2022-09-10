from flask import Blueprint, request, jsonify
from controllers.update_document_controller import UpdateDocumentController
from download_parsers.gifdroid_json_parser import gifdroidJsonParser
from flask_cors import cross_origin
from utility.safe_serialise import safe_serialize
from utility.uuid_generator import unique_id_generator

###############################################################################
#                            Set Up Flask Blueprint                           #
###############################################################################
update_document_blueprint = Blueprint("file", __name__)
file_controller = UpdateDocumentController('apk', gifdroidJsonParser)


@update_document_blueprint.route("/result/get/<uuid>/<algorithm>", methods=['GET'])
@cross_origin()
def get_result_of_algorithm(uuid, algorithm):
    """
    Method for getting a document from api
    """

    try:
        print("Starting get document")

        doc = file_controller.get_document(uuid)
        print(doc['results'][algorithm])

        result = doc['results'][algorithm]

        return result, 200
    except Exception as e:
        print(e)
        return str(e), 400


@update_document_blueprint.route("/result/get/<uuid>", methods=['GET'])
@cross_origin()
def get_document(uuid):
    """
    Method for getting a document from api
    """

    print("Starting get document")

    if request.method == "GET":
        return safe_serialize( file_controller.get_document(uuid) ), 200

    return "Invalid request", 400


@update_document_blueprint.route("/result/add/<uuid>/<algorithm>", methods=['GET', 'POST'])
@cross_origin()
def result_add(uuid, algorithm):
    """
    Method for adding result
    """
    if request.method == 'POST':
        ###############################################################################
        #                             Get the files array                             #
        ###############################################################################
        # Assume request json looks like this
        # example = {
        #     "files": ["{files}"],
        #     "type": "type"
        # }

        print(uuid)
        print(algorithm)
        links = request.json.get("files")
        type = request.json.get("type")
        file_names = request.json.get("names")
        print(type)

        file_controller.insert_algorithm_result(uuid, algorithm, links, type, file_names)

        return "Done", 200

    return "Invalid Request", 400



# @update_document_blueprint.route("/file/add", methods=['GET', "POST"])
# @cross_origin()
# def add_documment():
#     if request.method == "POST":
#         try:
#             ###############################################################################
#             #                         Add file metadata to mongodb                 #
#             ###############################################################################

#             document = data

#             for each_key, _ in document.items():
#                 document[each_key] = request.args.get(each_key)

#             document['uuid'] = unique_id_generator()
#             print(document)

#             mongo.insert_document(document, mongo.get_collection('apk')).inserted_id

#             return document['uuid'], 200
#         except Exception as e:
#             ###############################################################################
#             #                                Error Handling                       #
#             ###############################################################################
#             return str(e), 400


#     return "Not a valid request", 400


if __name__ == "__main__":
    pass
