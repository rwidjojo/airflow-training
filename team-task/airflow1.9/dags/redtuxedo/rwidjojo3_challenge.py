# Instruction:
# pass variable "username" from PythonOperator to function _print_context

import logging
from datetime import timedelta

import airflow
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.models import Variable

ownerJSON = Variable.get("owner_rwidjojo", deserialize_json=True) # Replace with your short name

owner = ownerJSON["name"]

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(5),
}

dag = DAG(
  dag_id=f'{owner}.lesson3.challenge',
  start_date=airflow.utils.dates.days_ago(5),
  schedule_interval=timedelta(days=4),
  default_args=default_args,
)

def write_to_log(varname, **kwargs):
    myText = kwargs[varname]
    logging.info(myText)
    print(myText)
    return myText

def calculate(**kwargs):
    ti = kwargs["ti"]
    a,b = ti.xcom_pull(key=None, task_ids=["prev_exec","next_exec"])
    print(b-a)

greet_task =  BashOperator(
    task_id="say_hello",
    bash_command='echo "Hi from Airflow!"',
    dag=dag,
)

get_prev_exec = PythonOperator(
    task_id="prev_exec",
    python_callable=write_to_log,
    provide_context=True,
    op_args=["prev_execution_date"],
    dag=dag,
)

get_next_exec = PythonOperator(
    task_id="next_exec",
    python_callable=write_to_log,
    provide_context=True,
    op_args=["next_execution_date"],
    dag=dag,
)

calc_interval = PythonOperator(
    task_id="calc_interval",
    python_callable=calculate,
    provide_context=True,
    dag=dag,
)

greet_task >> [get_prev_exec, get_next_exec] >> calc_interval