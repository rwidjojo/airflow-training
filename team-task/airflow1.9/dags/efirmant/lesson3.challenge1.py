#schedule interval is every 4 days, so DAG will be running each 4 days.
#Start date is 5 days ago
#There are 4 task greet_task, get_prev_exec, get_next_exec and calc_interval
#greet_task is just show greeting message using BashOperator
#get_prev_exec using PythonOperator get previous execution date and show it then pass to xcomm
#get_next_exec using PythonOperator get next execution date and show it then pass to xcomm
#calc_interval is get xcomm from get_prev_exec and get_next_exec then calculate duration between prev execution date and next execution date
#Task dependency:
#                   ->  get_prev_exec
#                  /                 \
#greet_task                     calc_interval
#                  \                 /
#                   -> get_next_exec



from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

owner = 'efirmant' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(5),
}

dag = DAG(
    f'{owner}.lesson3.challenge1',
    default_args=default_args,
    description='Read context, passing it then check difference',
    schedule_interval=timedelta(days=4),
)

greet_task = BashOperator(
    task_id="greet",
    bash_command=f'echo "Hello {owner}"',
    dag=dag,
)

def _get_prev_exec(prev_execution_date, next_execution_date, **kwargs):
  print
  logging.info(prev_execution_date)
  logging.info(next_execution_date)
  return prev_execution_date

get_prev_exec = PythonOperator(
  task_id="get_prev_exec",
  python_callable=_get_prev_exec,
  dag=dag,
  provide_context=True,
)


def _get_next_exec(prev_execution_date, next_execution_date, **kwargs):
  logging.info(prev_execution_date)
  logging.info(next_execution_date)
  return next_execution_date

get_next_exec = PythonOperator(
  task_id="get_next_exec",
  python_callable=_get_next_exec,
  dag=dag,
  provide_context=True,
)

def _calc_diff(ti, **kwargs):
  logging.info('complete task')
  prev_ed, next_ed = ti.xcom_pull(key=None, task_ids=['get_prev_exec', 'get_next_exec'])
  logging.info(prev_ed)
  logging.info(next_ed)
  delta = next_ed - prev_ed
  logging.info(f'Date diff is {delta.in_words()}')
  

calc_diff = PythonOperator(
  task_id="calc_diff",
  python_callable=_calc_diff,
  dag=dag,
  provide_context=True,
)


greet_task >> [get_prev_exec, get_next_exec] >> calc_diff