from celery import Celery, current_task
from celery.result import AsyncResult
import os

from enums.status_enum import StatusEnum as Status
from controllers.algorithm_status_controller import AlgorithmStatusController as ASC

worker = Celery(__name__)
worker.conf.broker_url = os.environ['REDIS_URL']
worker.conf.result_backend = os.environ['REDIS_URL']



###############################################################################
#                         Algorithm status controller                         #
###############################################################################
asc = ASC(collection_name='apk')


# @worker.task(name="run_algorithm")
# def run_algorithm(info={}):
#     pass
