#
# Instructions: 
# Set up this DAG tasks dependecy with requirement:
#  - t1 run first 
#  - after t1 finised then t2a, t2b and t2c could run in parallel
#  - after t2b finished then run t3
#  - after t2a, t2c and t3 finished then run t4


from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

owner = 'mf' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['m.fashol@sampoerna.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}
dag = DAG(
    f'{owner}.lesson1.excercise2',
    default_args=default_args,
    description='DAG with task dependencies variation',
    schedule_interval=None,
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

#
# Set task dependecy after this
#
#  - t1 run first 
#  - after t1 finised then t2a, t2b and t2c could run in parallel
t1 >>  [t2a, t2b, t2c]
#  - after t2b finished then run t3
t2b >> t3
#  - after t2a, t2c and t3 finished then run t4
[t2a, t2c, t3] >> t4