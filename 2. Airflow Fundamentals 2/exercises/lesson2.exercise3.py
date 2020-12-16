# Instructions
# Define a function that uses the python logger to log 
# a function. Then finish filling in the details of the 

import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator


owner = 'john_doe' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.lesson2.excercise3',
    default_args=default_args,
)

greet_task = PythonOperator(
    task_id="first_airflow_program",
    python_callable=first_prog,
    dag=dag
)
