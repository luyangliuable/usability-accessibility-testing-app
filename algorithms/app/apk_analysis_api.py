import shutil
from apk_analysis import ApkAnalysis
from models.screenshot import Screenshot
from resources.resource_types import ResourceType
from resources.resource import *
from flask import Flask, request, jsonify
import requests
import os
import json
import boto3
from tasks.xbot import Xbot
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
    _result_types = {
        'Xbot': ResourceType.ACCESSIBILITY_ISSUE,
        'Owleye': ResourceType.DISPLAY_ISSUE,
        'Tappability': ResourceType.TAPPABILITY_PREDICTION
    }

    def __init__(self, job_info) -> None:
        self.uuid = job_info['uuid']
        output_dir = os.path.join(ApkAnalysisApi._shared_volume, self.uuid)
        req_tasks = [name[0].upper() + name[1:] for name in list(job_info['algorithms'])]
        apk_path = job_info['apk_file']
        additional_files = job_info['additional_files']
        super().__init__(output_dir, apk_path, req_tasks, additional_files)
        self.results = {}
        self._init_results()
        self.running = set(self.req_tasks)
        
            
    def start_processing(self) -> None:
        self._init_results()
        for task in self.req_tasks:
            self._update_status("RUNNING", task.lower())
        super().start_processing(uuid=self.uuid)
    
    ####################### TEMP
    def test(self) -> None:
        self._init_results()
        self.running.add('tappable')
        for task in self.req_tasks:
            self._update_status("RUNNING", task.lower())
        
        xb = Xbot(os.path.join(self.output_dir, 'xbot'), self.resources, self.uuid)
        shutil.copytree('/home/data/test/a2dp.Vol_133/', f'/home/data/{self.uuid}/', dirs_exist_ok=True)
        xb._publish_outputs()
        time.sleep(5.0)
        self._update_status("SUCCESSFUL")
    
    def _init_results(self) -> None:
        """Subscribe to results resource events."""
        self.results["ui-states"] = {}
        for task in self.req_tasks:
            if not task in ApkAnalysisApi._result_types:
                continue
        self.resources[ApkAnalysisApi._result_types[task]].subscribe(self._new_result_callback)


    def _new_result_callback(self, resource: ResourceWrapper) -> None:
        origin = resource.get_origin()
        result = resource.get_metadata()
        
        if origin == 'Xbot':
            self._add_xbot_result(result)
        if origin == 'Owleye':
            self._add_owleye_result(result)
        if origin == 'Tappable':
            self._add_tappable_result(result)
    
    
    def _add_result(self, screenshot: Screenshot, name: str, result: dict) -> None:
        result_key = (screenshot.ui_screen, screenshot.structure_id)
        
        if result_key not in self.results:
            img_url = self._upload_file(screenshot.image_path)
            fields = {"activity-name": screenshot.ui_screen,
                      "structure-id": screenshot.structure_id,
                      "base-image": img_url}
            self.results["ui-states"][result_key] = fields
        
        self.results["ui-states"][result_key][name] = result
        self._post_results()
        
        resource_type = ApkAnalysisApi._result_types[name[0].upper() + name[1:]]
        if not self.resources[resource_type].is_active():
            self._update_status("SUCCESSFUL", name.lower())
            self.running.remove(name.lower())
        
        if len(list(self.running))==0:
            self._update_status("SUCCESSFUL")
    
    
    def _add_xbot_result(self, result):
        screenshot = result["screenshot"]
        img_url = self._upload_file(result["image_path"])
        with open(result["description_path"]) as f:
            desc = f.read()
        desc = desc.split('\n\n')
        issues = []
        for i in range(1, len(desc)):
            issue = desc[i].split('\n')
            if len(issue) != 3:
                continue
            element = issue[1]
            if element[0] == '[':
                element = f'Element at bounds {issue[1]}'
            issues.append({
                "issue_type": issue[0],
                "component_type": element,
                "issue_desc": issue[2]
                    })
        result = {"image": img_url, "description": issues}
        self._add_result(screenshot, "xbot", result)
        
    def _add_owleye_result(self, result):
        screenshot = result["screenshot"]
        # upload image file
        img_url = self._upload_file(result["image_path"])
        result = {"image": img_url}
        self._add_result(screenshot, "owleye", result)    
    
    def _add_tappable_result(self, result):
        screenshot = result["screenshot"]
        # upload image file
        img_url = self._upload_file(result["image_path"])
        with open(result["description_path"]) as f:
            desc = json.loads(f.read())
        heatmaps = []
        for path in result["heatmap"]:
            heatmaps.append(self._upload_file(path))
        result = {"image": img_url, "description": desc, "heatmaps": str(heatmaps)}
        self._add_result(screenshot, "tappable", result)    

        
    def _upload_file(self, path: str) -> str:
        """Uploads file and returns S3 url"""
        key = self.uuid + '/' + path.removeprefix(self.output_dir).lstrip('/')
        s3_client.upload_file(path, BUCKETNAME, key)
        return f'http://localhost:4566/{BUCKETNAME}/{key}'
    
    def _post_results(self) -> str:
        url = RESULT_URL+self.uuid
        data = {"ui-states": list(self.results["ui-states"].values())}
        
        response = None
        error = None

        try:
            request = requests.Session()
            response = request.post(url, headers={"Content-Type": "application/json"}, json=data)

        except Exception as e:
            error = str(e)
            print("ERROR ON REQUEST: " + error)
        
        print(response)
    
    def _update_status(self, status, algorithm=None) -> None:
        url = f'{STATUS_URL}{self.uuid}'
        data = {
            "status": status
            }
        
        if algorithm is not None:
            url = url+f'/{algorithm}'
            data["logs"] = 'complete'
        
        response = None
        error = None

        try:
            request = requests.Session()
            response = request.post(url, headers={"Content-Type": "application/json"}, json=data)

        except Exception as e:
            error = str(e)
            print("ERROR ON REQUEST: " + error)

        print(response)


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
        # job.start_processing()
        job.test()
        

        return jsonify( {"result": "SUCCESS"} ), 200

    return "No HTTP POST method received", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3050)
