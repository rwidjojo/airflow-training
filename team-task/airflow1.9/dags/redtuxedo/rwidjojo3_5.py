import datetime
import logging

from pprint import pprint
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

ownerJSON = Variable.get("owner_rwidjojo", deserialize_json=True) # Replace with your short name

owner = ownerJSON["name"]

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
    pprint(kwargs)

print_context = PythonOperator(
  task_id="print_context",
  python_callable=_print_context,
  provide_context=True,
  dag=dag,
)