import shutil
from apk_analysis import *
from models.screenshot import Screenshot
from resources.resource_types import ResourceType
from resources.resource import *
from flask import Flask, request, jsonify
import requests
import os
import json
import boto3
import time


RESULT_URL = 'http://host.docker.internal:5005/results/add/'
STATUS_URL = 'http://host.docker.internal:5005/status/update/'
AWS_PROFILE = 'localstack'
AWS_REGION = 'us-west-2'
S3_URL = 'http://host.docker.internal:4566'
BUCKETNAME = 'apk-bucket'

boto3.setup_default_session(profile_name=AWS_PROFILE)
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    endpoint_url=S3_URL,
)


class ApkAnalysisApi(ApkAnalysis):

    _shared_volume = '/home/data'
    _additional_file_types = {'Gifdroid': ResourceType.GIF, 'Uichecker': ResourceType.UI_RULES}

    def __init__(self, job_info) -> None:
        self.uuid = job_info['uuid']
        output_dir = os.path.join(ApkAnalysisApi._shared_volume, self.uuid)
        req_tasks = [name[0].upper() + name[1:] for name in list(job_info['algorithms'])]
        apk_path = job_info['apk_file']
        additional_files = job_info['additional_files']
        super().__init__(output_dir, apk_path, req_tasks, additional_files)
        self.uploaded_files = set()
        self.running = set()


    def start_processing(self) -> None:
        """To start processing the equation"""
        for task in self.req_tasks:
            self._update_status("RUNNING", task.lower())
            self.running.add(task)
        super().start_processing(uuid=self.uuid)


    def _update_utg(self, new_utg: dict) -> None:
        """Updates the UTG to MongoDB"""
        super()._update_utg(new_utg)
        self._post_utg(self.utg)


    def _add_result(self, result: dict, origin: str) -> None:
        """Uploads result to MongoDM and updates algorithm status"""
        super()._add_result(result, origin)
        self._post_task_result(result, origin)
        # update status
        r_type = ApkAnalysis._result_types[origin]
        if r_type and not self.resources[r_type].is_active():
            self._update_status(StatusEnum.successful, algorithm=origin)
            if origin in self.running:
                origin.remove(self.running)
        elif r_type:
            logs = f'{origin} published new result'
            self._update_status(StatusEnum.running, algorithm=origin, logs=logs)
        if len(list(self.running)) == 0:
            self._update_status(StatusEnum.successful)
    
            
    def _repl_filepaths(self, item: dict, _new_path: Callable[[str], str]=None) -> dict:
        return super()._repl_filepaths(item, self._upload_file)


    def _upload_file(self, path: str) -> str:
        """Uploads file and returns S3 url"""
        try:
            if path not in self.uploaded_files:
                key = path.removeprefix(self.output_dir).lstrip('/')
                s3_client.upload_file(path, BUCKETNAME, key)
                self.uploaded_files.add(path)
                file_url = f'http://localhost:4566/{BUCKETNAME}/{key}'
                print(f"Uploaded file {path} to S3 at {file_url}")
            return file_url

        except:
            print('ERROR UPLOADING TO S3')
            return path


    def _post_task_result(self, result: dict, task: str) -> str:
        url = os.path.join(RESULT_URL, self.uuid, task.lower())
        data = result
        response = None
        error = None
        try:
            request = requests.Session()
            response = request.post(url, headers={"Content-Type": "application/json"}, json=data)

        except Exception as e:
            error = str(e)
            print("ERROR ON POST RESULTS REQUEST: " + error)

        print(f"POST RESULTS. Response: {response}\n")
    
    def _post_utg(self, new_utg: dict) -> str:
        url = os.path.join(RESULT_URL, self.uuid, 'utg')
        data = new_utg
        
        response = None
        error = None
        try:
            request = requests.Session()
            response = request.post(url, headers={"Content-Type": "application/json"}, json=data)

        except Exception as e:
            error = str(e)
            print("ERROR ON POST RESULTS REQUEST: " + error)

        print(f"POST RESULTS. Response: {response}\n")
    
    def _update_status(self, status: StatusEnum, algorithm: str=None, logs: str=None) -> None:
        url = f'{STATUS_URL}{self.uuid}'
        data = {
            "status": status
            }

        if algorithm is not None:
            url = url+f'/{algorithm.lower()}'
            if logs is not None:
                data["logs"] = f'{logs}'
            else:
                data["logs"] = f'{algorithm.lower()} {status}'
                
        response = None
        error = None

        try:
            request = requests.Session()
            response = request.post(url, headers={"Content-Type": "application/json"}, json=data)
            print(f'UPDATED STATUS: {data.values()} {response}')

        except Exception as e:
            error = str(e)
            print("ERROR ON REQUEST: " + error)



app = Flask(__name__)

@app.route("/begin_apk_analysis", methods=["POST"])
def begin_apk_analysis():
    """
    This function begins running algorithms in the backend.

    POST req input:
    uid - The unique ID for tracking all the current task.
    algorithms - List of algorithms to be run
    apk_file - Path of apk file
    additional_files - Dictionary of additional files and their algorithms
    """
    if request.method == "POST":

        job = ApkAnalysisApi(request.get_json())
        job.start_processing()


        return jsonify( {"result": "SUCCESS"} ), 200

    return "No HTTP POST method received", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3050)