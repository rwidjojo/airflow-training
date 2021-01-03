import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

def hello_world():
    logging.info("Hello World")


def addition():
    result = 2+2
    logging.info(f"2 + 2 = {result}")
    return result

def subtraction():
    result = 6-2
    logging.info(f"6 -2 = {result}")
    return result


def division():
    result = int(10/2)
    logging.info(f"10 / 2 = {result}")
    return result

def completed_task(**kwargs):
    ti = kwargs['ti']
    ## Pull xcom here
    addition_res, subtraction_res, division_res = ti.xcom_pull(key=None, task_ids=['addition', 'subtraction', 'division'])
    summary = addition_res + subtraction_res + division_res
    logging.info(f"Summary from all task is {summary}")


owner = 'msantoso4' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.lesson2.excercise8',
    default_args=default_args,
)

hello_world_task = PythonOperator(
    task_id="hello_world",
    python_callable=hello_world,
    dag=dag,
)

addition_task = PythonOperator(
    task_id="addition",
    python_callable=addition,
    dag=dag,
)

subtraction_task = PythonOperator(
    task_id="subtraction",
    python_callable=subtraction,
    dag=dag,
)

division_task = PythonOperator(
    task_id="division",
    python_callable=division,
    dag=dag,
)

completed_task = PythonOperator(
    task_id="completed_task",
    python_callable=completed_task,
    provide_context=True,
    dag=dag,
)

hello_world_task >> [addition_task, subtraction_task, division_task] >> completed_task