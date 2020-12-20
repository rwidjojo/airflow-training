## Lesson 2 Exercise 8

**Instructions:**
Summary result from addition_task, division_task and subtraction_task

```python
import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


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
    summary = ....  # calculate xcom result here
    logging.info(f"Summary from all task is {summary}")


owner = 'john_doe' # Replace with your short name

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

hello_world_task >> [addition_task, substraction_task, division_task] >> completed_task
```

Code above declare DAG with 5 tasks `hello_world_task`,`addition_task`, `substraction_task`, `division_task` and completed_task.

- `hello_world_task` call python function to log `hello world`
- `addition_task` call python function that doing addition
- `substraction_task` call python function that doing substraction
- `division_task` call python function that doing division
- last `completed_task` has to summary result from `addition_task`, `substraction_task` and `division_task`

If you pay attention to `addition_task`, `substraction_task` and `division_task` then each task call python function that has `return` return statement `return result`. As mention on module **12. Cross-Task Communication** that return statement on python function will automatically register returned values to xcomm.

So in task `completed_task` we could use xcomm to pull resutl from these tasks.

```python
def completed_task(**kwargs):
    ti = kwargs['ti']
    ## Pull xcom here
    addition_res, subtraction_res, division_res = ti.xcom_pull(key=None, task_ids=['addition', 'substraction', 'division'])
    summary = addition_res + subtraction_res + division_res
    logging.info(f"Summary from all task is {summary}")
```

or

```python
def completed_task(**kwargs):
    ti = kwargs['ti']
    ## Pull xcom here
    addition_res = ti.xcom_pull(task_ids='addition')
    subtraction_res = ti.xcom_pull(task_ids='substraction')
    division_res = ti.xcom_pull(task_ids='division')
    summary = addition_res + subtraction_res + division_res
    logging.info(f"Summary from all task is {summary}")
```

### Complete Code Solution

```python
import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


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
    addition_res, subtraction_res, division_res = ti.xcom_pull(key=None, task_ids=['addition', 'substraction', 'division'])
    summary = addition_res + subtraction_res + division_res
    logging.info(f"Summary from all task is {summary}")


owner = 'john_doe' # Replace with your short name

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

hello_world_task >> [addition_task, substraction_task, division_task] >> completed_task
```
