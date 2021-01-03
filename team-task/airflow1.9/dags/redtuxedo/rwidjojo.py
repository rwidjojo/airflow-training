#
# Instructions: Find error in this code
#

from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

owner = 'rwidjojo' # Replace with your short name

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
    f'{owner}.lesson1.excercise1',
    default_args=default_args,
    description='DAG simple pipeline',
    schedule_interval='@daily',
)

t1 = BashOperator(
    task_id='rw_print_date',
    bash_command='date',
    dag=dag,
)

t2 = BashOperator(
    task_id='rw_sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    retries=3,
    dag=dag,
)

t3 = BashOperator(
    task_id='rw_final_task',
    depends_on_past=False,
    bash_command='echo "I am final task"',
    dag=dag,
)

t1 >> t2 >> t3