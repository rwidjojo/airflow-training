
# Instruction: 
# Run this DAG twice or more
#

from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.models import Variable

ownerJSON = Variable.get("owner_rwidjojo", deserialize_json=True) # Replace with your short name

owner = ownerJSON["name"]

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.lesson3.challenge3',
    default_args=default_args,
    description='Read data from postgresql using postgreshook and do grouping with python',
    schedule_interval=None,
)

def read_data():
    db_conn = PostgresHook(postgres_conn_id='rwidjojo_postgres_2')
    scriptsql = """
    SELECT order_id, order_date from rwidjojo_orders
    """
    result = db_conn.get_records(scriptsql)
    myDict = {}
    for row in result:
        if not row["order_date"] in myDict:
            myDict[row["order_date"]] = 1
        else:
            myDict[row["order_date"]] += 1
    
    print("order_date", "count_id")
    for key,val in myDict.items():
        print(key, val)
      # logging.info(row["order_date"], row["countid"])

wait_oltp_file = FileSensor(
    task_id="wait_oltp_file",
    filepath="/home/ubuntu/airflow/dags/redtuxedo/lesson34_2.sql",
    dag=dag,
    poke_interval=30,
    timeout=90,
    soft_fail=True,
)

read = PythonOperator(
    task_id="read",
    python_callable=read_data,
    dag=dag
)

wait_oltp_file >> read