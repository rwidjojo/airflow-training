# Instructions
# complete each task PythonOperator arguments

import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


def calculator(operator, number1, number2):
    if (operator == '+'):
        logging.info(f"{number1} + {number2} = {number1 + number2}")
    elif (operator == '-'):
        logging.info(f"{number1} - {number2} = {number1 - number2}")
    elif (operator == '*'):
        logging.info(f"{number1} * {number2} = {number1 * number2}")
    elif (operator == '/'):
        logging.info(f"{number1} / {number2} = {number1 / number2}")
    else:
        logging.info("operator not registered")

owner = 'mf' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.lesson2.excercise6',
    default_args=default_args,
)

addition_task = PythonOperator(
    task_id="addition_task",
    python_callable=calculator,
    op_kwargs={'operator': '+', 'number1': 2, 'number2': 9},
    dag=dag,
)

subraction_task = PythonOperator(
    task_id="subraction_task",
    python_callable=calculator,
       op_kwargs={'operator': '-', 'number1': 9, 'number2': 2},
    dag=dag,
)

multiplication_task = PythonOperator(
    task_id="multiplication_task",
    python_callable=calculator,
    op_kwargs={'operator': 'x', 'number1': 2, 'number2': 9},
    dag=dag,
)

division_task = PythonOperator(
    task_id="division_task",
    python_callable=calculator,
    op_kwargs={'operator': '/', 'number1': 2, 'number2': 9},
    dag=dag,
)

addition_task >> subraction_task >> multiplication_task >> division_task


