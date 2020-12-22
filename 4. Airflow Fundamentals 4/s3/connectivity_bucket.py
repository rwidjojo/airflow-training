import boto3
import logging
from botocore.exceptions import ClientError

AWS_KEY_ID='AKIAIFQGGJINGVFZR6SA'
AWS_SECRET='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'

try:
    s3 = boto3.client("s3", 
        region_name='ap-southeast-1', 
        aws_access_key_id=AWS_KEY_ID, 
        aws_secret_access_key=AWS_SECRET)
    # logging.info(s3)
    print(s3)
except ClientError as e:
    # logging.error(e)
    print(e)