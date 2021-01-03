#
# Instructions: Find error in this code
#

from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

owner = 'mf' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['mfaishol@sampoerna.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}
dagtes = DAG(
    f'{owner}.lesson1.excercise1',
    default_args=default_args,
    description='DAG simple pipeline',
    schedule_interval='@daily',
)

# assign task (t1, t2, t3)

t1 = BashOperator(
    task_id='print_date',  # unique tiap DAG
    bash_command='date',
    dag=dagtes,
)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    retries=0,
    dag=dagtes,
)

t3 = BashOperator(
    task_id='final_task',
    depends_on_past=False,
    bash_command='echo "I am final task"',
    dag=dagtes,
)

t1 >> t2 >> t3