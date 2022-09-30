from flask import jsonify, send_file
from celery import Celery, current_task
from celery.result import AsyncResult
import os
import requests

from enums.status_enum import StatusEnum as Status
from controllers.algorithm_status_controller import AlgorithmStatusController as ASC
from download_parsers.gifdroid_json_parser import gifdroidJsonParser

celery = Celery(__name__)
celery.conf.broker_url = os.environ['REDIS_URL']
celery.conf.result_backend = os.environ['REDIS_URL']

flask_backend = os.environ.get('FLASK_BACKEND')


###############################################################################
#                         Algorithm status controller                         #
###############################################################################
asc = ASC(collection_name='apk')


@celery.task(name="run_algorithm")
def run_algorithm(info={}):
    ###############################################################################
    #                                Storydistiller                               #
    ###############################################################################
    errors = []

    try:

        uuid = info["uuid"]
        algorithm_name = info['algorithm']

        update_status_url = os.path.join(str( flask_backend ), 'status', 'update', uuid, algorithm_name)

        # Story distiller api url to be obtained from the enrionemtn ###############
        story_distiller_api = os.environ.get("STORYDISTILLER")
        # xbot api url to be obtained from the enrionemtn ##########################
        xbot_api = os.environ.get("XBOT")
        # xbot api url to be obtained from the enrionemtn ##########################
        owleye_api = os.environ.get("OWLEYE")

        start_links = {
            "storydistiller": story_distiller_api,
            "xbot": xbot_api,
            "owleye": owleye_api,
            "gifdroid": os.environ['GIFDROID'],
            "tappable": "SKIP"
        }

        URL = start_links[algorithm_name]

        ###############################################################################
        #                      Print some usefull debugging info                      #
        ###############################################################################
        print(f'TASK: Running { str( algorithm_name ) } url: { str( URL ) }')
        print(f'TASK: Algorithm cluster uuid is { uuid }')

        ###############################################################################
        #                      Change algorithm status to started                     #
        ###############################################################################
        if URL != "SKIP":
            requests.post(update_status_url, headers={"Content-Type": "text/plain"}, data=Status.running.value )

        ###############################################################################
        #                          Signal Algorithm to start                          #
        ###############################################################################
        result = requests.post(str( URL ), json={ "uid": uuid })

        ###############################################################################
        #           Update status according to the success of the algorithm           #
        ###############################################################################
        if result.status_code < 400:
            requests.post(update_status_url, headers={"Content-Type": "text/plain"}, data=Status.successful )
            print("TASK: Successfully completed task", algorithm_name)
        else:
            print(f'TASK: algorithm url { update_status_url }.')
            requests.post(update_status_url, headers={"Content-Type": "text/plain"}, data=Status.failed )
            print("TASK: FAILED complete task", algorithm_name)

    except Exception as ex:
        algorithm_name = info['algorithm']
        print(f'TASK: failed to complete tasks with url { str( URL ) } because { ex }')
        errors.append(ex)
    else:
        state = {"task_id": "", "task_status": ['distiller'], "task_result": ""}

    result = {"files": ["file_url_placeholder"], "images": ["image_url_placeholder"], "errors": str( errors ) }
