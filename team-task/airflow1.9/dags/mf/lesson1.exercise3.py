#
# Instructions: 
# Change DAG schedule interval so DAG could automatically run every 30 minutes
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
    'email': ['m.fashol@sampoerna.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}
dag = DAG(
    f'{owner}.lesson1.excercise3',
    default_args=default_args,
    description='DAG simple pipeline',
    # Place schedule interval here
    schedule_interval='*/30 * * * *',
    catchup = True
)
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │
# │ │ │ │ │
# * * * * * <command to execute>

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)