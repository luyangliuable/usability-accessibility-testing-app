# Server Readme

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Server Readme](#server-readme)
    - [Purpose of this folder and flask app here](#purpose-of-this-folder-and-flask-app-here)
    - [About amazon s3 bucket](#about-amazon-s3-bucket)
        - [Requirements](#requirements)
        - [Credentials](#credentials)
        - [Configuration](#configuration)
        - [To create a bucket](#to-create-a-bucket)
        - [List all files in bucket](#list-all-files-in-bucket)
        - [Need to declare s3 endpoint as environment variable (done automatically in docker)](#need-to-declare-s3-endpoint-as-environment-variable-done-automatically-in-docker)

<!-- markdown-toc end -->

## Purpose of this folder and flask app here
* API for front end to connect with
* Upload functionality
* Trigger all other apps to run using API
* Task queues.

## About amazon s3 bucket

* Need to create credentials and configurations in ./aws folder

### Requirements
* Python3
* Localstack in python
* aws-cli


### Credentials
```
[localstack]
aws_access_key_id=#####
aws_secret_access_key=#####
```

### Configuration

```
[localstack]
region = us-west-2
output = json
```

### To create a bucket

```shell
aws --endpoint-url=http://localhost:4566 s3 mb s3://bucketname
```

### Copy a folder into s3 bucket

```shell
aws --endpoint-url=http://localhost:4566 s3 cp ./folder s3://bucketname/ --recursive
```

### List all files in bucket

```shell
aws --endpoint-url=http://localhost:4566 s3 ls s3://bucketname
```

### Delete all files in bucket
```
aws s3 --endpoint-url=http://localhost:4566 rm s3://apk-bucket/ --recursive --include "*"
```

### Delete all files in bucket excluding 1
```
sudo aws s3 rm s3://apk-bucket/ --recursive --include "*" --exclude "donotdelete.txt"
```

### Need to declare s3 endpoint as environment variable (done automatically in docker)


* Example only
```shell
    export S3_URL=http://127.0.0.1:4566
```
