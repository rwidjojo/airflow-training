
from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.latest_only_operator import LatestOnlyOperator
from airflow.operators.dummy_operator import DummyOperator


owner = 'efirmant' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(3),
}

dag = DAG(
    f'{owner}.lesson4.challenge2',
    default_args=default_args,
    description='Read data from postgresql',
    schedule_interval=None,
)

greet_task = BashOperator(
    task_id="greet",
    bash_command=f'echo "Hello {owner}"',
    dag=dag,
)

def _odd_process():
    print("odd branching")

def curr_date(execution_date,**kwargs):
    print(f"Execution date: {execution_date}")

def final_f():
    logging.info("DAG was run successfully")

def _pick_migration(**kwargs):
  execution_date = kwargs['execution_date']
  if execution_date.day % 2 != 0:
    return 'branch_odd' # returning task id `branch_odd`
  else:
    return 'branch_even' # returning task id `branch_even`


branching_task = BranchPythonOperator(
  task_id='migration_branch',
  provide_context=True,
  python_callable=_pick_migration,
  dag=dag
)

branch_odd_task = BashOperator(
    task_id="branch_odd",
    bash_command=f'echo "Odd Day"',
    dag=dag,
)

branch_even_task = BashOperator(
    task_id="branch_even",
    bash_command=f'echo "Even Day"',
    dag=dag,
)

odd_process_task = PythonOperator(
    task_id="odd_process",
    python_callable=_odd_process,
    dag=dag,
)

curr_date_task = PythonOperator(
    task_id="curr_date",
    python_callable=curr_date,
    provide_context=True,
    dag=dag,
    trigger_rule='none_failed',
)

final_task = PythonOperator(
    task_id="final_task",
    python_callable=final_f,
    dag=dag,
)

is_latest_task = LatestOnlyOperator(
    task_id="is_latest",
    dag=dag
)

dummy_notif_task = DummyOperator(
    task_id="dummy_notif",
    dag=dag
)

greet_task >> branching_task >> [branch_even_task, branch_odd_task]
branch_odd_task >> odd_process_task
[branch_even_task, odd_process_task] >> curr_date_task >> final_task >> is_latest_task >> dummy_notif_task

#greet_task => task that say hello
#branching_task => task that decide flow where DAG run
##branch_odd_task => task that only run when execution_date is odd number
#branch_even_task => task that only run when execution_date is even number
#odd_process_task => task that run after branch_odd_task finished
#curr_date_task => task that run after odd_process_task or branch_even_task and print current execution date
#final_task => task that run after curr_date_task and log that dag is success.
#is_latest_task => task that check if execution date is latest run
#notif_task => dummy notification that DAG has run successfully and only run is_latest_task running successfully
