3# Instruction 
# - after migrate data successfully 
# - create new task to read how many records inserted on table `shipping_count`
# - log the result


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
    f'{owner}.lesson4.exercise3',
    default_args=default_args,
    description='Read data from postgresql',
    schedule_interval=None,
)

def insert_data(ds, **kwargs):
  # declare connection
  db_conn = PostgresHook(postgres_conn_id='john_doe_postgres')

  # declare sql string
  sql = f"""
  SELECT order_date, ship_country, COUNT(order_id) ship_count
  FROM public.recent_orders
  WHERE order_date = '{ds}'
  GROUP BY order_date, ship_country
  ORDER BY order_date
  """

  # log formatted sql so it easier to debug
  logging.info(sql)

  # execute sql
  result = db_conn.get_records(sql)

  # declare insert sql 
  insert_sql = """
  INSERT INTO public.shipping_count(order_date, ship_country, ship_count)
  VALUES(%s, %s, %s)
  ON CONFLICT (order_date, ship_country)
  DO NOTHING;
  """
  # insert each row to table `public.shipping_count`
  for row in result:
    db_conn.run(
    insert_sql,
    parameters=(
        row['order_date'],
        row['ship_country'],
        row['ship_count'])
    )


insert_task = PythonOperator(
    task_id="InsertData",
    python_callable=insert_data,
    provide_context=True,
    dag=dag,
)


def count_data(ds, **kwargs):
  # declare connection
  db_conn = PostgresHook(postgres_conn_id='john_doe_postgres')

  # declare sql string
  sql = f"""
  SELECT  COUNT(order_date) ship_count
  FROM public.shipping_count
  WHERE order_date = '{ds}'
  """

  logging.info(sql)
  result = db_conn.get_records(sql)

  for rec in result:
      logging.info(rec)

# instruction:
# declare new task to count how many records inserted that day
count_task = PythonOperator(
    task_id="rowcount",
    python_callable=count_data,
    provide_context=True,
    dag=dag,
)
insert_task >> count_task