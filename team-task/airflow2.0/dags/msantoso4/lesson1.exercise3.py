  
#
# Instructions: 
# Change DAG schedule interval so DAG could automatically run every 30 minutes
#

from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

owner = 'msantoso4' # Replace with your short name

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
    f'{owner}.lesson1.excercise3',
    default_args=default_args,
    description='DAG simple pipeline',
    # Place schedule interval here
    schedule_interval=  '*/1 * * * *'
)

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)