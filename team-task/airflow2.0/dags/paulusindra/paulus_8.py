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


owner = 'paulusindra' # Replace with your short name

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
    op_kwargs={'operator':'+','number1':111,'number2':123}, # fill argument addition calculation here
    dag=dag,
)

subtraction_task = PythonOperator(
    task_id="subtraction_task",
    python_callable=calculator,
    op_kwargs={'operator':'-','number1':111,'number2':123}, # fill argument addition calculation here
    dag=dag,
)

multiplication_task = PythonOperator(
    task_id="multiplication_task",
    python_callable=calculator,
    op_kwargs={'operator':'*','number1':12345678987654321,'number2':111111111}, # fill argument multiplication calculation here
    dag=dag,
)

division_task = PythonOperator(
    task_id="division_task",
    python_callable=calculator,
    op_kwargs={'operator':'/','number1':12345678987654321,'number2':111111111}, # fill argument multiplication calculation here
    dag=dag,
)

addition_task >> subtraction_task >> multiplication_task >> division_task


