import boto3
import logging
from botocore.exceptions import ClientError

AWS_KEY_ID='AKIAIFQGGJINGVFZR6SA'
AWS_SECRET='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'
bucket_name = "john-doe-pmi"
file_name = "Bitcoin.csv"
file_path = "archive/"
# region = ""
region = 'ap-southeast-1'

try:
    s3 = boto3.resource(
        's3',
        aws_access_key_id=AWS_KEY_ID, 
        aws_secret_access_key=AWS_SECRET)
        
    store_bucket = s3.meta.client.upload_file(file_name, bucket_name, file_name)
    # ExtraArgs={'ACL': 'public-read'}
    print(store_bucket)
except ClientError as e:
    print(e)