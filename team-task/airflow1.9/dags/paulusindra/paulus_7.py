
# Instructions
# Define a function that uses the python logger to log 
# parameter from PythonOperator 

import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


owner = 'paulusindra' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.lesson2.excercise5',
    default_args=default_args,
)

def write_to_log(**kwargs):
    print(kwargs)
    return kwargs['log_to_write']
    
greet_task = PythonOperator(
    task_id="say_hello",
    python_callable=write_to_log,
    op_kwargs={'log_to_write': f'Hi {owner} greeting from airflow','halo':'ini parameter2'},
    dag=dag,
)

bye_task = PythonOperator(
    task_id="bye_hello",
    python_callable=write_to_log,
    op_kwargs={'log_to_write': 'Good bye'},
    dag=dag,
)

greet_task >> bye_task

