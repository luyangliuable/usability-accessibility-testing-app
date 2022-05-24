import boto3
import os
import subprocess
from PIL import Image


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

    _upload_result(uuid, name)

    # restore original source code
    subprocess.run(["rm", "-r", "/home/OwlEye-main"])
    subprocess.run(["cp", "-r", "/home/tmp/OwlEye-main", "/home/OwlEye-main"])
    subprocess.run(["rm", "-r", "/home/tmp/OwlEye-main"])

# get the inputs from s3
def _get_data(uuid):
    raw_dir = '/home/OwlEye-main/png_pic/'
    filepath = '/home/OwlEye-main/input_pic/'
    s3.download_file('storydistiller-bucket', uuid+'/screenshots', raw_dir)
    _process_png_to_jpg(raw_dir,filepath)

# Process pictures from png to jpeg
def _process_png_to_jpg(raw_dir, image_dir):
    """
    Using PIL converts images from png to jpg
    """
    raw_pics = os.listdir(raw_dir)
    for raw_png in raw_pics:
        (filename, extension) = os.path.splitext(raw_png)
        if extension != ".txt":
            raw_png_dir = raw_dir + raw_png
            pil_jpg = Image.open(raw_png_dir, mode='r')

            pil_jpg__dir = image_dir + filename+".jpg"
            pil_jpg.convert('RGB').save(pil_jpg__dir,'JPEG')

# run the algorithm
def _process_result():
    os.chdir("/home/OwlEye-main")
    subprocess.run(["python3", "localization.py"])
    os.chdir("/home/app")

# upload results to s3
def _upload_result(uuid, name):

    bucketname = "owleye-bucket"
    folder_name = "%s/screenshots/" % uuid

    dirpath = "/home/OwlEye-main/output_pics"
    
    for (root, _, filenames) in os.walk(dirpath):
        for file in filenames:
            filelocal = os.path.join(root,file)
            filebucket = os.path.join(folder_name, file)
            print(filebucket)
            s3.upload_file(filelocal, bucketname, filebucket)

            s3.generate_presigned_url(
            'get_object',
            Params = {'Bucket': bucketname, 'Key': filebucket},
            ExpiresIn = 1000
            )
            


if __name__=='__main__':
    # test run
    # service_execute('a2dp.Vol_133.apk', 'a2dp.Vol_133.apk')
    _process_png_to_jpg('/home/OwlEye-main/png_pic/','/home/OwlEye-main/input_pic/')


