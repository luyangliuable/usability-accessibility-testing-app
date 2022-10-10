from apk_analysis import ApkAnalysis
from resources.screenshot import Screenshot
from resources.resource_types import ResourceType
from flask import Flask, request, jsonify
import os
import json

class ApkAnalysisApi:

    _algorithm_outputs = {
    }

    # _algorithm_outputs = {
    #     'Xbot': [ResourceType.ACCESSABILITY_ISSUE, Screenshot],
    #     'Tappability': [Screenshot]
    # }

    _shared_volume = '/home/data'

    def __init__(self, json):
        self.algorithm_execution_json_metadata = json
        self.req_results = []
        self._run()


    def _run(self):
        uuid = self.algorithm_execution_json_metadata['uuid']
        output_dir = os.path.join(self._shared_volume, uuid)
        names = self.algorithm_execution_json_metadata['algorithms']
        apk_file = self.algorithm_execution_json_metadata['apk_file']
        additional_files = self.algorithm_execution_json_metadata['additional_files']
        analysis = ApkAnalysis(output_dir, names, apk_file, additional_files)
        analysis.start_processing(uuid)


    def _init_req_results(self) -> None:
        """Adds required results for each algorithm"""
        for algo in self.algorithm_execution_json_metadata['algorithms']:
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3050)
