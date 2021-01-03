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
    f'{owner}.lesson4.excercise2',
    default_args=default_args,
    description='Insert data from postgresql',
    schedule_interval=None,
)

def migrate_data():
  src_conn = PostgresHook(postgres_conn_id='efirmant_postgres')
  dest_conn = PostgresHook(postgres_conn_id='efirmant_postgres')
  result = src_conn.get_records(sql = """
  SELECT order_date, ship_country, COUNT(order_id) ship_count
  FROM public.recent_orders
  GROUP BY order_date, ship_country
  ORDER BY order_date
  """)

  insert_sql = """
    INSERT INTO shipping_count(order_date, ship_country, ship_count) VALUES(%s, %s, %s) ON CONFLICT (order_date, ship_country) DO NOTHING;"""
  for row in result:
    logging.info(insert_sql)
    dest_conn.run(insert_sql, parameters=(row['order_date'],row['ship_country'],row['ship_count']))

migrate_task = PythonOperator(
    task_id="migrate",
    python_callable=migrate_data,
    dag=dag
)