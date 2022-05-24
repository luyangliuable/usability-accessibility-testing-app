
import uu
import boto3
import os
import subprocess


AWS_REGION = 'us-west-2'
AWS_PROFILE = 'localstack'
ENDPOINT_URL = os.environ.get('S3_URL')

boto3.setup_default_session(profile_name=AWS_PROFILE)

s3 = boto3.client("s3", region_name=AWS_REGION,
                         endpoint_url=ENDPOINT_URL)


def service_execute(uuid, name):

    # backup original source code
    subprocess.run(["cp", "-r", "/home/OwlEye-main", "/home/tmp/OwlEye-main"])

    _get_data(uuid, name)

    _process_result()

    _upload_result(uuid)

    # restore original source code
    subprocess.run(["rm", "-r", "/home/OwlEye-main"])
    subprocess.run(["cp", "-r", "/home/tmp/OwlEye-main", "/home/OwlEye-main"])
    subprocess.run(["rm", "-r", "/home/tmp/OwlEye-main"])

# get the inputs from s3
def _get_data(uuid, name):
    filepath = '/home/OwlEye-main/input_pic/' + name
    s3.download_file('storydistiller-bucket', uuid, filepath)

    # TODO
    # extract PNG pics from zip file and convert to jpeg and delete the zip file after

# run the algorithm
def _process_result():
    os.chdir("/home/OwlEye-main")
    subprocess.run(["python3", "localization.py"])
    os.chdir("/home/app")

# upload results to s3
def _upload_result(uuid):
    pass

if __name__=='__main__':
    # test run
    service_execute('a2dp.Vol_133.apk.zip', 'a2dp.Vol_133.apk.zip')

