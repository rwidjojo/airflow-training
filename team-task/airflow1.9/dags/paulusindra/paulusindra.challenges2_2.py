from datetime import timedelta
import logging
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.latest_only_operator import LatestOnlyOperator
from airflow.operators.dummy_operator import DummyOperator

vOwn = Variable.get('owner_paulusindra', deserialize_json=True)
owner = vOwn['name']
args = {
    'owner': owner,
    'start_date': days_ago(4)
}

dag = DAG(
    f'{owner}.challenges2_2',
    default_args=args,
    schedule_interval='@daily',
)

greet_task=BashOperator(
    task_id='greet_task',
    bash_command=f'echo Hi, welcome to DAG Challenges 2 for {owner}',
    dag=dag
)

def _branching_task(**kwargs):
    execution_date = kwargs['execution_date'].day
    if (execution_date % 2 == 0):
        return 'branch_even_task'
    else:
        return 'branch_odd_task'

branching_task=BranchPythonOperator(
    task_id='branching_task',
    python_callable=_branching_task,
    provide_context=True,
    dag=dag
)

branch_odd_task=BashOperator(
    task_id='branch_odd_task',
    bash_command='echo "it\'s odd day"',
    dag=dag
)

branch_even_task=BashOperator(
    task_id='branch_even_task',
    bash_command='echo "it\'s even day"',
    dag=dag
)

odd_process_task=BashOperator(
    task_id='odd_process_task',
    bash_command='echo "it\'s odd task"',
    dag=dag
)

def _curr_date_task(**kwargs):
    execution_date=kwargs['execution_date']
    print(f'Execution Date is {execution_date}')

curr_date_task=PythonOperator(
    task_id='curr_date_task',
    python_callable=_curr_date_task,
    provide_context=True,
    trigger_rule='none_failed',
    dag=dag
)

def _final_task():
    logging.info("DAG is success")

final_task=PythonOperator(
    task_id='final_task',
    python_callable=_final_task,
    provide_context=True,
    dag=dag,
)

is_latest_task=LatestOnlyOperator(
    task_id='is_latest_task',
    dag=dag,
)

notif_task=DummyOperator(
    task_id='notif_task',
    dag=dag,
)

greet_task >> branching_task >> [branch_even_task, branch_odd_task]
branch_odd_task >> odd_process_task
[branch_even_task, odd_process_task] >> curr_date_task >> final_task >> is_latest_task >> notif_task