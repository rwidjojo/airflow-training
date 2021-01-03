from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

owner = 'dtjayain' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.lesson3.challenge2',
    default_args=default_args,
    description='Count data from postgresql',
    schedule_interval=None,
)

def count_Data():
  # declare connection
  db_conn = PostgresHook(postgres_conn_id='dtjayain_postgress')

  # declare sql string
  sql = f"""
  SELECT order_date, count(order_id) as count_id from dtjayain_orders
  GROUP BY order_date
  ORDER BY order_date ASC
  """

  # log formatted sql so it easier to debug
  logging.info(sql)

  # execute sql
  result = db_conn.get_records(sql)

  # log each row result
  for row in result:
    print(row["order_date"],row["count_id"])
    logging.info(row["order_date"], row["count_id"])


read_task = PythonOperator(
    task_id="count",
    python_callable=count_data,
    dag=dag
)