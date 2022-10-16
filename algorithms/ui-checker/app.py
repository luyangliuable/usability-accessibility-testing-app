import boto3
import os
import subprocess
import pathlib
from flask import Flask, request, jsonify

app = Flask(__name__)

# aws info for development environment
AWS_REGION = 'us-west-2'
AWS_PROFILE = 'localstack'
ENDPOINT_URL = os.environ.get('S3_URL')

# aws s3 client
boto3.setup_default_session(profile_name=AWS_PROFILE)
s3_client = boto3.client("s3", region_name=AWS_REGION,
                         endpoint_url=ENDPOINT_URL)

# home route
@app.route('/')
def home():
    return "ui-checker app is live."

# route for starting new job
@app.route("/execute", methods=["POST"])
def execute():
    if request.method == "POST":
        try:
            apk_path = request.get_json()["apk_path"]
            dl_path = request.get_json()["dl_path"]
        except:
            return 'Invalid uuid data', 500

        _process_result(apk_path, dl_path)
        out_path = _upload_result(apk_path)
        return jsonify( {"result": "SUCCESS", "out_path":out_path} ), 200

    return "No HTTP POST method received", 500


# run the algorithm
def _process_result(apk_name, dl_name):
    os.chdir("/home/ui-checker")
    subprocess.run(["./uicheck", apk_name, dl_name])
    akp_file_name = os.path.basename(apk_name)
    os.chdir("/home/ui-checker/output_markii/%s.apk/" %apk_file_name)

# upload results to s3
def _upload_result(apk_name):
    akp_file_name = os.path.basename(apk_name)
    bucket = 'ui-checker-bucket'
    output_root_path = '/home/ui-checker/output_markii/%s.apk/' %apk_file_name

    # upload output folder zip
    output_filename = 'ui-checker_output_%s.zip' %apk_file_name
    os.chdir(output_root_path)
    os.system('zip -r %s %s' % (output_filename, apk_file_name))

    output_folder_path = output_root_path + output_filename
    return output_folder_path

if __name__=='__main__':
    app.run(debug=True, host="0.0.0.0", port=3069)
    # test run
    #_service_execute('a2dp.Vol_133')
