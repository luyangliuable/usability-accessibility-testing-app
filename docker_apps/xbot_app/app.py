
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
    subprocess.run(["cp", "-r", "/home/Xbot-main", "/home/tmp/Xbot-main"])

    _get_data(uuid, name)

    _process_result()

    _upload_result(uuid)

    # restore original source code
    subprocess.run(["rm", "-r", "/home/Xbot-main"])
    subprocess.run(["cp", "-r", "/home/tmp/Xbot-main", "/home/Xbot-main"])
    subprocess.run(["rm", "-r", "/home/tmp/Xbot-main"])

# get the inputs from s3
def _get_data(uuid, name):
    filepath = '/home/Xbot-main/main-folder/apks/' + name
    s3.download_file('apk-bucket', uuid, filepath)

# run the algorithm
def _process_result():
    os.chdir("/home/Xbot-main/code")
    subprocess.run(["python", "run_xbot.py"])
    os.chdir("/home/app")

# upload results to s3
def _upload_result(uuid):
    pass


if __name__=='__main__':
    
    # test run
    service_execute('a2dp.Vol_133.apk', 'a2dp.Vol_133.apk')

