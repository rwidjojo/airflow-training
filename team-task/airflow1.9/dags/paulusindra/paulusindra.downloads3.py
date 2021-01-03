from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable

from datetime import datetime, timedelta
import boto3
import logging

vOwn = Variable.get('owner_paulusindra', deserialize_json=True)
owner = vOwn['name']
# default arguments for each task
default_args = {
    'owner': f'{owner}',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


dag = DAG(f'{owner}.download_s3',
          default_args=default_args,
          schedule_interval=None)  # "schedule_interval=None" means this dag will only be run by external commands

TEST_BUCKET = 'pmi-airflow'
TEST_BUCKET = 'pmi-airflow/Salim_Paulus_Indra'
TEST_KEY = 'pmi.txt'
LOCAL_FILE = f'/home/ubuntu/airflow/dags/{owner}/pmi.txt'


# simple download task
def download_file(bucket,destination):
    s3 = boto3.resource('s3',
         aws_access_key_id='AKIAIFQGGJINGVFZR6SA',
         aws_secret_access_key='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')
    try:
        s3.Bucket(TEST_BUCKET).download_file(TEST_KEY, 'my_local_image.jpg')
    except :
        logging.info("The object does not exist.")

# simple upload task
def upload_file(source, bucket):
    s3 = boto3.resource('s3',
         aws_access_key_id='AKIAIFQGGJINGVFZR6SA',
         aws_secret_access_key='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')
    # s3.Bucket(bucket).upload_file(source)
    
    s3.meta.client.upload_file(LOCAL_FILE, bucket, 'hello.txt')


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

# download_from_s3.set_downstream(sleep_task)
# sleep_task.set_downstream(upload_to_s3)