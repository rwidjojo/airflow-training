## Lesson 2 Exercise 4

**Instructions:**
Compose task so DAG become like this

```
                    ->  addition_task
                   /                 \
 hello_world_task  -> division_task-> completed_task
                   \                 /
                    -> subtraction_task
```

**Code:**

```python
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


owner = 'john_doe' # Replace with your short name

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
```

Code above declare DAG with 5 tasks:

- `hello_world_task` call python function `hello_world`
- `addition_task` call python function `addition`
- `subtraction_task` call python function `substraction`
- `division_task` call python function `division`
- `completed_task` call python function `completed_task`

to make DAG became like this:

```
                    ->  addition_task
                   /                 \
 hello_world_task  -> division_task-> completed_task
                   \                 /
                    -> subtraction_task
```

then we need set task dependency like this

```python
hello_world_task >> [addition_task, subtraction_task, division_task] >> completed_task
```

or

```python
hello_world_task >> addition_task
hello_world_task >> subtraction_task
hello_world_task >> division_task
addition_task >> completed_task
subtraction_task >> completed_task
division_task >> completed_task
```

**Complete Code Solution:**

```python
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


owner = 'john_doe' # Replace with your short name

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

hello_world_task >> [addition_task, subtraction_task, division_task] >> completed_task
```
