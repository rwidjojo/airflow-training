import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable


owner = Variable.get("owner_msantoso4") # Replace with your short name

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
    print(kwargs)
    return kwargs['return log to write']

greet_task = PythonOperator(
    task_id="say_hello",
    python_callable=say_hello,
    op_kwargs={'log_to_write': f'Hi {owner} greeting from airflow'},
    dag=dag,
)

bye_task = PythonOperator(
    task_id="say_bye",
    python_callable=say_hello,
    op_kwargs={'log_to_write': 'Good bye'},
    dag=dag,
)

greet_task >> bye_task