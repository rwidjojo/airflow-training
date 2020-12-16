#
# Instructions: 
# See how depend_on_past works

from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

owner = 'john_doe' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}
dag = DAG(
    f'{owner}.lesson1.excercise2',
    default_args=default_args,
    description='DAG with task dependencies variation',
    schedule_interval='@daily',
)

t1 = BashOperator(
    task_id='task1',
    bash_command='echo "task 1 executed"',
    dag=dag,
)

t2a = BashOperator(
    task_id='task2a',
    bash_command='echo "task 2a executed"',
    dag=dag,
)

t2b = BashOperator(
    task_id='task2b',
    bash_command='echo "task 2b executed"',
    dag=dag,
    depends_on_past=True,
    wait_for_downstream=True,
)

t2c = BashOperator(
    task_id='task2c',
    bash_command='echo "task 2c executed"',
    dag=dag,
)

t3 = BashOperator(
    task_id='task3',
    bash_command='echo "task 3 executed"',
    dag=dag,
)

t4 = BashOperator(
    task_id='task4',
    bash_command='echo "task 4 executed"',
    dag=dag,
)

t1 >> [t2a, t2b, t2c] 
t2b >> t3
[t2a, t2c, t3] >>t4