# Instructions
# create airflow variable through web ui then
# replace owner below using variable from airflow

import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

owner = Variable.get("owner_dtjayain", deserialize_json=True) # Replace with your short name

default_args = {
    'owner': owner["name"],
    'depends_on_past': False,
    'start_date': days_ago(2),
}

def say_hello(**kwargs):
    logging.info(kwargs["log_to_write"])

dag = DAG(
    f'{owner["name"]}.lesson2.excercise7',
    default_args=default_args,
)

greet_task = PythonOperator(
    task_id="say_hello",
    python_callable=say_hello,
    op_kwargs={'log_to_write': f'Hi {owner["name"]} greeting from airflow'},
    dag=dag,
)

bye_task = PythonOperator(
    task_id="bye_hello",
    python_callable=say_hello,
    op_kwargs={'log_to_write': 'Good bye'},
    dag=dag,
)

greet_task >> bye_task