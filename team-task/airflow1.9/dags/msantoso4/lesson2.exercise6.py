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

owner = 'msantoso4' # Replace with your short name

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
    op_kwargs={'operator': '+', 'number1': 10, 'number2': 5},
    dag=dag,
)

subtraction_task = PythonOperator(
    task_id="subtraction_task",
    python_callable=calculator,
    op_kwargs={'operator': '-', 'number1': 7, 'number2': 4},
    dag=dag,
)

multiplication_task = PythonOperator(
    task_id="multiplication_task",
    python_callable=calculator,
    op_kwargs={'operator': '*', 'number1': 3, 'number2': 2},
    dag=dag,
)

division_task = PythonOperator(
    task_id="division_task",
    python_callable=calculator,
    op_kwargs={'operator': '/', 'number1': 10, 'number2': 5},
    dag=dag,
)

addition_task >> subtraction_task >> multiplication_task >> division_task