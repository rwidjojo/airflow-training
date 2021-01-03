#
# Instructions:
#
#                    ->  addition_task
#                   /                 \
# hello_world_task  -> division_task-> completed_task                
#                   \                 /
#                    -> subtraction_task



import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


def hello_world():
    logging.info("Hello World")


def addition():
    logging.info(f"2 + 2 = {2+2}")


def subtraction():
    logging.info(f"6 -2 = {6-2}")


def division():
    logging.info(f"10 / 2 = {int(10/2)}")
 
def completed_task():
    logging.info("All Tasks Completed")


owner = 'efirmant' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.lesson2.excercise4',
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
    dag=dag,
)
#
#                    ->  addition_task
#                   /                 \
# hello_world_task  -> division_task-> completed_task                
#                   \                 /
#                    -> subtraction_task