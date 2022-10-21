import boto3
import os

###############################################################################
#                                  Set Up AWS                                 #
###############################################################################
AWS_PROFILE = 'localstack'
AWS_REGION = 'us-west-2'
ENDPOINT_URL = os.environ.get('S3_URL')
BUCKETNAME = "apk-bucket"

boto3.setup_default_session(profile_name=AWS_PROFILE)
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    endpoint_url=ENDPOINT_URL
)

def enforce_bucket_existance(buckets):
    for bucket in buckets:
        try:
            s3_client.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
        except:
            print("Bucket already exists %s".format( bucket ))
