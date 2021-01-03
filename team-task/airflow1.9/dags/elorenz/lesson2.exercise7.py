# Instructions
# create airflow variable through web ui then
# replace owner below using variable from airflow

import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable


owner = Variable.get("owner_elorenz") # Replace with your short name
#owner = 'elorenz'

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.lesson2.excercise7',
    default_args=default_args,
)

def say_hello(**kwargs):
  logging.info('log_to_write')
  print('log_to_write')
   # return kwargs

def say_goodbye(**kwargs):
  logging.info('writing_log')
   # return kwargs

greet_task = PythonOperator(
    task_id="say_hello",
    python_callable=say_hello,
    op_kwargs={'log_to_write': f'Hi {owner} greeting from airflow'},
    dag=dag,
)

bye_task = PythonOperator(
    task_id="say_goodbye",
    python_callable=say_goodbye,
    op_kwargs={'writing_log': 'Good bye'},
    dag=dag,
)

greet_task >> bye_task