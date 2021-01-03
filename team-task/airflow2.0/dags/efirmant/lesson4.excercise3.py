from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

owner = 'efirmant' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.lesson4.excercise3',
    default_args=default_args,
    description='Insert data from postgresql',
    schedule_interval=None,
)

def migrate_data(ds, **kwargs):
  src_conn = PostgresHook(postgres_conn_id='efirmant_postgres')
  dest_conn = PostgresHook(postgres_conn_id='efirmant_postgres')
  result = src_conn.get_records(sql = f"""
  SELECT order_date, ship_country, COUNT(order_id) ship_count
  FROM public.recent_orders
  WHERE order_date = '{ds}'
  GROUP BY order_date, ship_country
  ORDER BY order_date
  """)

  insert_sql = """
    INSERT INTO shipping_count(order_date, ship_country, ship_count) VALUES(%s, %s, %s) ON CONFLICT (order_date, ship_country) DO NOTHING;"""
  for row in result:
    logging.info(insert_sql)
    dest_conn.run(insert_sql, parameters=(row['order_date'],row['ship_country'],row['ship_count']))


def read_data(ds, **kwargs):
 # declare connection
  db_conn = PostgresHook(postgres_conn_id='efirmant_postgres')

  # declare sql string
  sql = f"""
  SELECT order_date, ship_country, ship_count
  FROM shipping_count
  WHERE order_date = '{ds}'
  ORDER BY order_date
  """

  # log formatted sql so it easier to debug
  logging.info(sql)

  # execute sql
  result = db_conn.get_records(sql)

  # log each row result
  for row in result:
    logging.info(row)




migrate_task = PythonOperator(
    task_id="migrate",
    python_callable=migrate_data,
    provide_context=True,
    dag=dag
)

read_task = PythonOperator(
    task_id="read",
    python_callable=read_data,
    provide_context=True,
    dag=dag
)