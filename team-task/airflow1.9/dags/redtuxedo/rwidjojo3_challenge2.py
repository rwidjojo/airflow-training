
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
    f'{owner}.lesson3.challenge2',
    default_args=default_args,
    description='Read data from postgresql using postgresqloperator',
    schedule_interval=None,
)

def read_data():
    db_conn = PostgresHook(postgres_conn_id='rwidjojo_postgres_2')
    sqlfile = open('/home/ubuntu/airflow/dags/redtuxedo/lesson34_2.sql','r')
    sqlscript = sqlfile.read()
    sqlfile.close()
    # scriptsql = """
    # SELECT order_date, count(order_id) as countid from rwidjojo_orders
    # GROUP BY order_date
    # ORDER BY order_date ASC;
    # """
    result = db_conn.get_records(sqlscript)
    for row in result:
        print(row["order_date"],row["count"])
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