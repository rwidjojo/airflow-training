# Instructions
# create airflow variable through web ui then
# replace owner below using variable from airflow

import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

vOwn = Variable.get("owner_paulusindra", deserialize_json=True)

owner = vOwn["name"] # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    '{0}.lesson2.excercise7'.format(owner),
    default_args=default_args,
)

def say_hello(**kwargs):
    print(kwargs)
    return kwargs['log_to_write']

greet_task = PythonOperator(
    task_id="say_hello",
    python_callable=say_hello,
    op_kwargs={'log_to_write': f'Hi {owner} greeting from airflow'},
    dag=dag,
)

bye_task = PythonOperator(
    task_id="bye",
    python_callable=say_hello,
    op_kwargs={'log_to_write': 'Good bye'},
    dag=dag,
)

bash_task = BashOperator(
    task_id="testbash",
    bash_command='echo "{0}"'.format(vOwn),
    dag=dag,
)
greet_task >> bye_task

