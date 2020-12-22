import boto3
import logging
import botocore
from botocore.exceptions import ClientError

AWS_KEY_ID='AKIAIFQGGJINGVFZR6SA'
AWS_SECRET='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'
bucket_name = "john-doe-pmi"
region = 'ap-southeast-1'
object_name = "Bitcoin.csv"


try:
    s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_KEY_ID, 
            aws_secret_access_key=AWS_SECRET,
            region_name=region)
    try:
        bucket_policy = s3.get_bucket_policy(Bucket=bucket_name)
        print(bucket_policy['Policy'])
    except ClientError as e:
        print(e)
except ClientError as e:
    print(e)