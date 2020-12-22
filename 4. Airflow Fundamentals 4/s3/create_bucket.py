import boto3
import logging
from botocore.exceptions import ClientError

AWS_KEY_ID='AKIAIFQGGJINGVFZR6SA'
AWS_SECRET='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'
bucket_name = "john-doe-pmi"

# region = ""
region = 'ap-southeast-1'

try:
    if region is None:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_KEY_ID, 
            aws_secret_access_key=AWS_SECRET)
        create_bucket = s3_client.create_bucket(Bucket=bucket_name)
        print(create_bucket)
    else:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_KEY_ID, 
            aws_secret_access_key=AWS_SECRET,
            region_name=region)
        location = {'LocationConstraint': region}
        create_bucket = s3_client.create_bucket(Bucket=bucket_name,
                                CreateBucketConfiguration=location)
        print(create_bucket)
except ClientError as e:
    print(e)