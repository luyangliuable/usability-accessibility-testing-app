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
        for task in self.req_tasks:
            self._update_status("RUNNING", task.lower())
            self.running.add(task)
        super().start_processing(uuid=self.uuid)

    def _update_utg(self, new_utg: dict) -> None:
        return super()._update_utg(new_utg)
    
    def _add_result(self, result: dict, origin: str) -> None:
        super()._add_result(result, origin)
        self._post_results()
        if not self.resources[ApkAnalysis._result_types[origin]].is_active():
            self._update_status(StatusEnum.successful, origin)
            if origin in self.running:
                origin.remove(self.running)
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


    def _post_results(self) -> str:
        url = RESULT_URL+self.uuid
        data = self.results
        
        response = None
        error = None
        try:
            request = requests.Session()
            response = request.post(url, headers={"Content-Type": "application/json"}, json=data)
            
        except Exception as e:
            error = str(e)
            print("ERROR ON POST RESULTS REQUEST: " + error)
            
        print(f"POST RESULTS. Response: {response}\n")
    
    def _post_utg(self) -> str:
        pass
    
    def _update_status(self, status, logs: str=None, algorithm=None) -> None:
        url = f'{STATUS_URL}{self.uuid}'
        data = {
            "status": status
            }

        if algorithm is not None:
            url = url+f'/{algorithm}'
            if logs:
                data["logs"] = f'{logs}'
            else:
                logs = f'{algorithm} {status}'
                
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
        # job.test()


        return jsonify( {"result": "SUCCESS"} ), 200

    return "No HTTP POST method received", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3050)


    # def test(self) -> None:
    #     for task in self.req_tasks:
    #         self._update_status("RUNNING", task.lower())

    #     rg = ResourceGroup(ResourceType.APK_FILE)
    #     self.resources[ResourceType.APK_FILE] = rg
    #     rg.publish(self.apk_resource, True)
    #     time.sleep(5.0)
    #     xb = Xbot(os.path.join(self.output_dir, 'xbot'), self.resources, self.uuid)
    #     shutil.copytree('/home/data/test/a2dp.Vol_133/', f'/home/data/{self.uuid}/', dirs_exist_ok=True)
    #     ow = Owleye(os.path.join(self.output_dir, 'owleye'), self.resources, self.uuid)
    #     xb._publish_outputs()

    # def _init_results(self) -> None:
    #     """Subscribe to results resource events."""
    #     self.results["ui-states"] = {}
    #     for task in self.req_tasks:
    #         if task in ApkAnalysisApi._result_types:
    #             self.running.add(task)
    #             self.resources[ApkAnalysisApi._result_types[task]].subscribe(self._new_result_callback)


    # def _new_result_callback(self, resource: ResourceWrapper) -> None:
    #     origin = resource.get_origin()
    #     result = resource.get_metadata()

    #     if origin == 'Xbot':
    #         self._add_xbot_result(result)
    #     if origin == 'Owleye':
    #         self._add_owleye_result(result)
    #     if origin == 'Tappable':
    #         self._add_tappable_result(result)


    # def _add_result(self, screenshot: Screenshot, name: str, result: dict) -> None:
    #     result_key = (screenshot.ui_screen, screenshot.structure_id)

    #     if result_key not in self.results["ui-states"]:
    #         img_url = self._upload_file(screenshot.image_path)
    #         fields = {"activity-name": screenshot.ui_screen,
    #                   "structure-id": screenshot.structure_id,
    #                   "base-image": img_url}
    #         self.results["ui-states"][result_key] = fields

    #     self.results["ui-states"][result_key][name] = result
    #     self._post_results()

    #     name = name[0].upper() + name[1:]
    #     resource_type = ApkAnalysisApi._result_types[name]
    #     if not self.resources[resource_type].is_active():
    #         self._update_status("SUCCESSFUL", name.lower())
    #         if name in self.running:
    #             self.running.remove(name)

    #     if len(list(self.running))==0:
    #         self._update_status('SUCCESSFUL')
    #         print(self.results)


    # def _add_xbot_result(self, result):
    #     screenshot = result["screenshot"]
    #     img_url = self._upload_file(result["image_path"])
    #     result = {"image": img_url, "description": result["description"]}
    #     self._add_result(screenshot, "xbot", result)

    # def _add_owleye_result(self, result):
    #     screenshot = result["screenshot"]
    #     # upload image file
    #     img_url = self._upload_file(result["image_path"])
    #     result = {"image": img_url}
    #     self._add_result(screenshot, "owleye", result)

    # def _add_tappable_result(self, result):
    #     screenshot = result["screenshot"]
    #     # upload image file
    #     img_url = self._upload_file(result["image_path"])
    #     heatmaps = []
    #     for path in result["heatmap"]:
    #         heatmaps.append(self._upload_file(path))
        
    #     desc_list = []
    #     for item in result['description']:
    #         desc_list.append(item)
            
    #     result = {"image": img_url, "description": desc_list, "heatmaps": heatmaps}
    #     self._add_result(screenshot, "tappable", result)