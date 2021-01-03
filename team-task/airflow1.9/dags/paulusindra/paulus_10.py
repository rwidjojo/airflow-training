#
# Instructions:
# Summary result from addition_task, division_task and subtraction_task


import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.models import XCom

vOwner = Variable.get("owner_paulusindra", deserialize_json=True)
owner = vOwner["name"] # Replace with your short name

args = {
    'owner': owner,
    'dependes_on_past': True,
    'start_date': days_ago(1)
}

def hello_world():
    logging.info("Hello World")


def addition(**kwargs):
    result = 2+2
    logging.info(f"2 + 2 = {result}")
    kwargs['ti'].xcom_push(key='addition', value=result)
    return result


def subtraction(**kwargs):
    result = 6-2
    logging.info(f"6 -2 = {result}")
    kwargs['ti'].xcom_push(key='subtraction', value=result)
    return result


def division(**kwargs):
    result = int(10/2)
    logging.info(f"10 / 2 = {result}")
    kwargs['ti'].xcom_push(key='division', value=result)
    return result
 
def completed_task(**kwargs):
    ti = kwargs['ti']
    # Pull xcom here 
    num1 = ti.xcom_pull(task_ids='addition')
    num2 = ti.xcom_pull(task_ids='subtraction')
    num3 = ti.xcom_pull(task_ids='division')
    summary = num1+num2+num3
    logging.info(f"Number from addition is {num1}")
    logging.info(f"Number from subtraction is {num2}")
    logging.info(f"Number from division is {num3}")
    logging.info(f"Summary from all task is {summary}")
    
dag = DAG(
    f'{owner}.lesson2.excercise8',
    default_args=args,
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
    provide_context=True,
)

subtraction_task = PythonOperator(
    task_id="subtraction",
    python_callable=subtraction,
    dag=dag,
    provide_context=True,
)

division_task = PythonOperator(
    task_id="division",
    python_callable=division,
    dag=dag,
    provide_context=True,
)

completed_task = PythonOperator(
    task_id="completed_task",
    python_callable=completed_task,
    provide_context=True,
    dag=dag,
)

hello_world_task >> [addition_task, subtraction_task, division_task] >> completed_task
# hello_world_task >> addition_task >> completed_task