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
        presigned_url = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name})
        print(presigned_url)


    except ClientError as e:
        print(e)

except ClientError as e:
    print(e)