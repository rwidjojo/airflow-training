# Instruction:
# Run this DAG twice or more
#

from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.postgres_operator import PostgresOperator
from airflow.contrib.sensors.file_sensor import FileSensor


owner = 'dtjayain' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.lesson3.excercise4',
    default_args=default_args,
    description='Read data from postgresql using postgresqloperator',
    schedule_interval=None,
)

wait_oltp_file = FileSensor(
    task_id="wait_oltp_file",
    filepath="/home/ubuntu/airflow/dags/dtjayain/lesson3.exercise4.sql",
    dag=dag,
    poke_interval=30,
    timeout=3600
)

write_to_postgres = PostgresOperator(
    task_id="write_to_postgres",
    postgres_conn_id="dtjayain_postgress2",
    sql="lesson3.exercise4.sql",
    dag=dag,
)

wait_oltp_file >> write_to_postgres