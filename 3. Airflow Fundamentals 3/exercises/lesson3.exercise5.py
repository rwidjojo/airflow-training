import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


owner = 'john_doe' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.lesson3.excercise5',
    default_args=default_args,
)

def _print_context(**kwargs):
  print(kwargs)

print_context = PythonOperator(
  task_id="print_context",
  python_callable=_print_context,
  provide_context=True,
  dag=dag,
)
