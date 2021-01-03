from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

owner = 'elorenz' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.lesson3.excercise2',
    default_args=default_args,
    description='Read data from postgresql',
    schedule_interval=None,
)

def migrate_data():
  src_conn = PostgresHook(postgres_conn_id='elorenz_postgres')
  dest_conn = PostgresHook(postgres_conn_id='elorenz_postgres2')
  result = src_conn.get_records('select * from public.orders limit 10')
  insert_sql = f"""
    INSERT INTO public.{owner}_orders(order_id,customer_id,employee_id,order_date,required_date,shipped_date,ship_via,freight,ship_name,ship_address,ship_city,ship_region,ship_postal_code,ship_country)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (order_id)
    DO NOTHING;
  """
  for row in result:
    logging.info(insert_sql)
    dest_conn.run(insert_sql, parameters=(row['order_id'],row['customer_id'],row['employee_id'],row['order_date'],row['required_date'],row['shipped_date'],row['ship_via'],row['freight'],row['ship_name'],row['ship_address'],row['ship_city'],row['ship_region'],row['ship_postal_code'],row['ship_country']))

migrate_task = PythonOperator(
    task_id="migrate",
    python_callable=migrate_data,
    dag=dag
)