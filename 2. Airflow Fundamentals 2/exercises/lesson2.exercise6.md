## Lesson 2 Exercise 6

**Instructions:**
complete each task PythonOperator arguments

```python
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

owner = 'john_doe' # Replace with your short name

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
    op_kwargs={}, # fill argument addition calculation here
    dag=dag,
)

subtraction_task = PythonOperator(
    task_id="subtraction_task",
    python_callable=calculator,
    op_kwargs={}, # fill argument subraction calculation here
    dag=dag,
)

multiplication_task = PythonOperator(
    task_id="multiplication_task",
    python_callable=calculator,
    op_kwargs={}, # fill argument multiplication calculation here
    dag=dag,
)

division_task = PythonOperator(
    task_id="division_task",
    python_callable=calculator,
    op_kwargs={}, # fill argument division calculation here
    dag=dag,
)

addition_task >> subtraction_task >> multiplication_task >> division_task
```

Code above declare DAG with 4 tasks `addition_task`, `subraction_task`, `multiplication_task` and `division_task`. All task is call same python function `calculator`.

Function calculator is simple naive function that do calculation based on arguments received. It has 3 arguments `operator`, `number1` and `number2`.

- if `operator` value is `+` then it will do `number1 + number2`
- if `operator` value is `-` then it will do `number1 - number2`
- if `operator` value is `*` then it will do `number1 * number2`
- if `operator` value is `/` then it will do `number1 / number2`
- if `operator` value is neither listed above then show log `operator not registered`

Because `addition_task` has `addition` in the name, then it should do `addition` too

```python
addition_task = PythonOperator(
    task_id="addition_task",
    python_callable=calculator,
    op_kwargs={'operator': '+', 'number1': 10, 'number2': 5},
    dag=dag,
)
```

Because `subtraction_task` has `subtraction` in the name, then it should do `subtraction` too

```python
subtraction_task = PythonOperator(
    task_id="subtraction_task",
    python_callable=calculator,
    op_kwargs={'operator': '-', 'number1': 7, 'number2': 4},
    dag=dag,
)
```

Because `multiplication_task` has `multiplication` in the name, then it should do `multiplication` too

```python
multiplication_task = PythonOperator(
    task_id="multiplication_task",
    python_callable=calculator,
    op_kwargs={'operator': '*', 'number1': 3, 'number2': 2},
    dag=dag,
)
```

Because `division_task` has `division` in the name, then it should do `division` too

```python
division_task = PythonOperator(
    task_id="division_task",
    python_callable=calculator,
    op_kwargs={'operator': '/', 'number1': 10, 'number2': 5},
    dag=dag,
)
```

**Complete Code Solution:**

```python
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

owner = 'john_doe' # Replace with your short name

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
```
