import boto3
import logging
import botocore
from botocore.exceptions import ClientError
import json

AWS_KEY_ID='AKIAIFQGGJINGVFZR6SA'
AWS_SECRET='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'
bucket_name = "john-doe-pmi"
region = 'ap-southeast-1'
object_name = "Bitcoin.csv"
bucket_policy = {
    'Version': '2012-10-17',
    'Statement': [{
        'Sid': 'AddPerm',
        'Effect': 'Allow',
        'Principal': '*',
        'Action': ['s3:GetObject'],
        'Resource': f'arn:aws:s3:::{bucket_name}/*'
    }]
}

bucket_policy = json.dumps(bucket_policy)
print(bucket_policy)

try:
    s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_KEY_ID, 
            aws_secret_access_key=AWS_SECRET,
            region_name=region)
    try:
        set_bucket_policy = s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
        print(set_bucket_policy)
    except ClientError as e:
        print(e)
except ClientError as e:
    print(e)