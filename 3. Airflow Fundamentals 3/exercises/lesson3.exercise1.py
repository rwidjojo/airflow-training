from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

owner = 'john_doe' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.lesson3.excercise1',
    default_args=default_args,
    description='Read data from postgresql',
    schedule_interval=None,
)

def read_data():
  db_conn = PostgresHook(postgres_conn_id='john_doe_postgres')
  result = db_conn.get_records('select * from public.orders limit 10')
  for row in result:
    logging.info(row)
    logging.info(row['order_id'])


read_task = PythonOperator(
    task_id="read",
    python_callable=read_data,
    dag=dag
)


