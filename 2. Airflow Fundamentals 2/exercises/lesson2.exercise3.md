## Lesson 2 Exercise 3

**Instructions:**
Define a function that uses the python logger to log
a function. Then finish filling in the details of the

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
    f'{owner}.lesson2.excercise3',
    default_args=default_args,
)

greet_task = PythonOperator(
    task_id="first_airflow_program",
    python_callable=first_prog,
    dag=dag
)
```

Code above is define a DAG that has singgle task `greet_task` with operator **Python Operator**.

```python
dag = DAG(
    f'{owner}.lesson2.excercise3',
    default_args=default_args,
)

greet_task = PythonOperator(
    task_id="first_airflow_program",
    python_callable=first_prog,
    dag=dag
)
```

Task `greet_task` has line `python_callable=first_prog` that mean it will call [python function](https://docs.python.org/3/reference/compound_stmts.html#function-definitions) with name `first_prog`, but that function not yet exists. So we need to declare it first

```python
def first_prog:
  # do something here
```

As instructed, function `first_prog` required to log something to console. In python to we can use [`logging` pacakage](https://docs.python.org/3/howto/logging.html)

```python
import logging
logging.info('Hello world')
```

if we combine it to function declaration then became

```python
import logging

def first_prog:
  logging.info('Hello world')
```

If `PythonOperator` want to call function above then the function need to be declared before task declaration

```python
def first_prog:
  logging.info('Hello world')

greet_task = PythonOperator(
    task_id="first_airflow_program",
    python_callable=first_prog,
    dag=dag
)
```

So complete DAG code become like this:

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
    f'{owner}.lesson2.excercise3',
    default_args=default_args,
)

def first_prog:
  logging.info('Hello world')

greet_task = PythonOperator(
    task_id="first_airflow_program",
    python_callable=first_prog,
    dag=dag
)
```
