# Instruction: 
# Run this DAG twice or more
#

from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.postgres_operator import PostgresOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.models import Variable

vOwn = Variable.get("owner_paulusindra", deserialize_json=True)

owner = vOwn["name"] # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.challenges_2',
    default_args=default_args,
    description='Read data from postgresql using postgresqloperator',
    schedule_interval=None,
)

wait_oltp_file = FileSensor(
    task_id="wait_oltp_file",
    filepath="/home/ubuntu/airflow/dags/paulusindra/paulusindra.challenges_2.sql",
    dag=dag,
    poke_interval=30,
    timeout=3600
)

count_order_per_order_date = PostgresOperator(
    task_id="count_order_per_order_date",
    postgres_conn_id="paulusindra_postgres_target",
    sql="paulusindra.challenges_2.sql",
    dag=dag,
)

wait_oltp_file >> count_order_per_order_date