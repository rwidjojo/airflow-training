# Incremental with Interval
# Based on lesson4.exercise1.py create new DAG with specs:
# DAG run each 2 day
# Instead of count daily order change to count 2 day order.

from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable

ownerJSON = Variable.get("owner_rwidjojo", deserialize_json=True) # Replace with your short name
owner = 'dtjayain' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(5),
}

dag = DAG(
    f'{owner}.lesson4.challenge1',
    default_args=default_args,
    description='Read data from postgresql',
    schedule_interval=timedelta(days=2),
)

def read_data(ds, execution_date, **kwargs):
  # declare connection
  db_conn = PostgresHook(postgres_conn_id='dtjayain_postgress')
  
  prev_date = execution_date.subtract(days=1).strftime("%Y-%m-%d")

  # declare sql string
  sql = f"""
  SELECT order_date, ship_country, COUNT(order_id) ship_count
  FROM public.recent_orders
  WHERE order_date >= '{prev_date}' AND order_date <= '{ds}'
  GROUP BY order_date, ship_country
  ORDER BY order_date
  """

  # log formatted sql so it easier to debug
  logging.info(sql)

  # execute sql
  result = db_conn.get_records(sql)

  countid = 0
  
  # log each row result
  for row in result:
    logging.info(row)
    countid = countid + row ['ship_count']

  logging.info(f"Total rows: {countid}")

read_task = PythonOperator(
    task_id="read",
    python_callable=read_data,
    provide_context=True,
    dag=dag
)