from algorithms.app.apk_analysis import ApkAnalysis
from resources.screenshot import Screenshot
from resources.resource_types import ResourceType
from flask import Flask, request, jsonify

import uuid
import json

class ApkAnalysisApi:
    
    _algorithm_outputs = {
        'Xbot': [ResourceType.ACCESSABILITY_ISSUE, Screenshot],
        'Tappability': [Screenshot]
    }
    
    def __init__(self, json):
        self.json_app = json
        self.req_results = []
        self._run()
    
    def _run(self):
        output_dir = '/home/data' + self.json_app['uid']
        names = self.json_app['algorithms']
        apk_file = self.json_app['apk_file']
        ApkAnalysis(output_dir, names, self.req_results, apk_file)
        ApkAnalysis.start_processing()
        
    def _init_req_results(self) -> None:
        """Adds required results for each algorithm"""
        for algo in self.json_app['algorithms']:
            for output in ApkAnalysisApi._algorithm_output[algo]:
                if output not in self.req_results:
                    self.req_results.append(output)


app = Flask(__name__)
@app.route("/begin_apk_analysis", methods=["POST"])
def begin_apk_analysis():
    """
    This function begins running algorithms in the backend.

    POST req input:
    uid - The unique ID for tracking all the current task.
    algorithms - List of algorithms to be run
    apk_file - Path of apk file
    """
    if request.method == "POST":
       
        ApkAnalysisApi(request.get_json())

        return jsonify( {"result": "SUCCESS"} ), 200

    return "No HTTP POST method received", 400