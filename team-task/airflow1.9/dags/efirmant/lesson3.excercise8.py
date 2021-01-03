# Instruction:
# pass variable "username" from PythonOperator to function _print_context

import logging

import airflow
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator


owner = 'efirmant' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
  dag_id=f'{owner}.lesson3.excercise8',
  start_date=airflow.utils.dates.days_ago(3),
  schedule_interval=None,
)

def _print_context(username, email,  **kwargs):
  ts = kwargs['ts']
  execution_date = kwargs['execution_date']
  year, month, *_ = execution_date.timetuple()

  logging.info(f'Hello {username}')
  logging.info(f'execution date is {ts} with year {year} and month {month:02}')

print_context = PythonOperator(
  task_id="print_context",
  python_callable=_print_context,
  dag=dag,
  provide_context=True,
  op_args=["efirmant","ericorachmad.firmanto@sampoerna.com"],
  op_kwargs={"fullname": "erico firmanto"},
)