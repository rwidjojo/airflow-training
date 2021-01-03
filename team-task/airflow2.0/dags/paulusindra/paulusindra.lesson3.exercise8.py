# Instruction:
# pass variable "username" from PythonOperator to function _print_context

import logging

import airflow
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable

vOwn = Variable.get("owner_paulusindra", deserialize_json=True)

owner = vOwn["name"] # Replace with your short name


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

def _print_context(username,username2,username3,email, **kwargs):
  ts = kwargs['ts']
  execution_date = kwargs['execution_date']
  fullname = kwargs['fullname']
  year, month, *_ = execution_date.timetuple()

  logging.info(f'Hello {username} {username2} {username3} {email}')
  logging.info(f'execution date is {ts} with year {year} and month {month:02}, good job {fullname}!')

print_context = PythonOperator(
  task_id="print_context",
  python_callable=_print_context,
  dag=dag,
  provide_context=True,
  op_args=["paulus","indra","salim","paulusindra.salim@sampoerna.com"],
  op_kwargs={"fullname": "paulus indra salim"},
)