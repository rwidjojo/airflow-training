# Instruction 
# after read data then insert data to table `shipping_count`

from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

owner = 'msantoso4' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(3),
}

dag = DAG(
    f'{owner}.lesson4.excercise2',
    default_args=default_args,
    description='Read data from postgresql',
    schedule_interval=None,
)

def migrate_data(ds, **kwargs):
  # declare connection
  db_conn = PostgresHook(postgres_conn_id='msantoso4_postgree')
  dest_conn =PostgresHook(postgres_conn_id='msantoso4_postgree')
  
  # declare sql string
  insert_sql = f"""
  INSERT INTO public.shipping_count(order_date, ship_country, ship_count)
  VALUES(%s, %s, %s)
  ON CONFLICT (order_date, ship_country)
  DO NOTHING;
  """
   # declare sql string
  sql = f"""
  SELECT order_date, ship_country, COUNT(order_id) ship_count
  FROM public.recent_orders
  WHERE order_date = '{ds}'
  GROUP BY order_date, ship_country
  ORDER BY order_date
  """

  # execute sql
  result = db_conn.get_records(sql)

    # log each row result
  for row in result:
      logging.info(row)

  for row in result:
      logging.info(insert_sql)
      dest_conn.run(
          insert_sql,
          parameters=(
            row['order_date'],
            row['ship_country'],
            row['ship_count'])
      )

migrate_task = PythonOperator(
    task_id="migrate",
    python_callable=migrate_data,
    provide_context=True,
    dag=dag,
)