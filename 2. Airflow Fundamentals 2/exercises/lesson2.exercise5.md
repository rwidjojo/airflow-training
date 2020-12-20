## Lesson 2 Exercise 5

**Instructions:**
Define a function that uses the python logger to log parameter from PythonOperator

```python
import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


owner = 'john_doe' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.lesson2.excercise5',
    default_args=default_args,
)

greet_task = PythonOperator(
    task_id="say_hello",
    python_callable=write_to_log,
    op_kwargs={'log_to_write': f'Hi {owner} greeting from airflow'},
    dag=dag,
)

bye_task = PythonOperator(
    task_id="bye_hello",
    python_callable=write_to_log,
    op_kwargs={'log_to_write': 'Good bye'},
    dag=dag,
)

greet_task >> bye_task
```

Code above describe DAG with 2 tasks `greet_task` and `bye_task`. Both tasks call same function `write_to_log`, same argument `log_to_write` but have different value.

Because function `write_to_log` not yet exist then we need to declare it first

```python
def write_to_log():
  logging.info(...)
```

Don't forget function `write_to_log` has argument `write_to_log`:

```python
def write_to_log(write_to_log):
  logging.info(write_to_log)
```

or we could define it like this:

```python
def write_to_log(**kwargs):
  logging.info(kwargs['write_to_log'])
```

**Complete Code Solution:**

```python
import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


owner = 'john_doe' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
    f'{owner}.lesson2.excercise5',
    default_args=default_args,
)

def write_to_log(write_to_log):
  logging.info(write_to_log)

greet_task = PythonOperator(
    task_id="say_hello",
    python_callable=write_to_log,
    op_kwargs={'log_to_write': f'Hi {owner} greeting from airflow'},
    dag=dag,
)

bye_task = PythonOperator(
    task_id="bye_hello",
    python_callable=write_to_log,
    op_kwargs={'log_to_write': 'Good bye'},
    dag=dag,
)

greet_task >> bye_task
```
