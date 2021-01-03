# Instruction 
# refactor DAG below so SQL script could query data incrementally

from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

owner = 'mf' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(3),
}

dag = DAG(
    f'{owner}.lesson4.challenge2',
    default_args=default_args,
    description='Read data from postgresql',
    schedule_interval=None,
)

def read_data():
  # declare connection
  db_conn = PostgresHook(postgres_conn_id='john_doe_postgres')

  # declare sql string
  sql = """
  SELECT order_date, ship_country, COUNT(order_id) ship_count
  FROM public.recent_orders
  WHERE order_date = '{ds}'
  GROUP BY order_date, ship_country
  ORDER BY order_date
  """

  # log formatted sql so it easier to debug
  loggin.info(sql)

  # execute sql
  result = db_conn.get_records(sql)

  # log each row result
  for row in result:
    logging.info(row)


read_task = PythonOperator(
    task_id="read",
    python_callable=read_data,
    dag=dag
)


