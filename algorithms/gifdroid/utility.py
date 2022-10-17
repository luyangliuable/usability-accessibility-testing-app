import boto3
import json
import os

endpoint_url = os.environ.get("S3_URL")

with open("config.json", "r") as f:
    config = json.load(f)

boto3.setup_default_session(profile_name=config[ 'AWS_PROFILE' ])
s3_client = boto3.client(
    "s3",
    region_name=config['AWS_REGION'],
    endpoint_url=endpoint_url,
)

def enforce_bucket_existance(buckets):
    for bucket in buckets:
        try:
            s3_client.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
        except:
            print("Bucket already exists %s".format( bucket ))
