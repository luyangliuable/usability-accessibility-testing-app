### How to seed data for s3 bucket (not Mongodb)

```shell
aws --endpoint-url=http://localhost:4566 s3 cp ./folder s3://bucketname/ --recursive
```
