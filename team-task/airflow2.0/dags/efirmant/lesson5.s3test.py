from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta
import boto3
import logging

owner = 'efirmant'

# default arguments for each task
default_args = {
    'owner': 'efirmant',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


dag = DAG(f'{owner}.lesson5.s3test',
          default_args=default_args,
          schedule_interval=None)  # "schedule_interval=None" means this dag will only be run by external commands

TEST_BUCKET = 'pmi-airflow'
TEST_KEY = 'pmi.txt'
LOCAL_FILE = '/home/ubuntu/airflow/airflow/dags/efirmant/pmi.txt'


# simple download task
def download_file(bucket,destination):
    s3 = boto3.resource('s3',
         aws_access_key_id='AKIAIFQGGJINGVFZR6SA',
         aws_secret_access_key='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')
    try:
        s3.Bucket(TEST_BUCKET).download_file(TEST_KEY, '/home/airflow/airflow/dags/efirmant/my_local_image.jpg')
    except :
        logging.info("The object does not exist.")

# simple upload task
def upload_file(source, bucket):
    s3 = boto3.resource('s3',
         aws_access_key_id='AKIAIFQGGJINGVFZR6SA',
         aws_secret_access_key='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')
    # s3.Bucket(bucket).upload_file(source)
    
    s3.meta.client.upload_file(LOCAL_FILE, bucket, TEST_KEY)


download_from_s3 = PythonOperator(
    task_id='download_from_s3',
    python_callable=download_file,
    op_kwargs={'bucket': TEST_BUCKET, 'destination': LOCAL_FILE},
    dag=dag)



sleep_task = BashOperator(
    task_id='sleep_for_1',
    bash_command='sleep 1',
    dag=dag)


upload_to_s3 = PythonOperator(
    task_id='upload_to_s3',
    python_callable=upload_file,
    op_kwargs={'bucket': TEST_BUCKET, 'source': LOCAL_FILE},
    dag=dag)

download_from_s3>>sleep_task>>upload_to_s3
