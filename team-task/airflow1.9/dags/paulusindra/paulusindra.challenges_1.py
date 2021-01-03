from datetime import timedelta
from datetime import datetime
import logging
import pendulum
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.models import Variable

vOwner = Variable.get("owner_paulusindra", deserialize_json=True)
owner = vOwner["name"]

default_args = {
    'owner': owner,
    'start_date': days_ago(5),
    'depends_on_past': False,
}

dag = DAG(
    dag_id='{0}.challenges'.format(owner),
    default_args=default_args,
    schedule_interval=timedelta(days=4),
)

def getPrevExecutionTime(**kwargs):
    prev_execution_date = kwargs['prev_execution_date']
    logging.info(f'Previous Execution Date Success is {prev_execution_date}')
    return prev_execution_date

def getNextExecutionTime(**kwargs):
    next_execution_date = kwargs['next_execution_date']
    logging.info(f'Next Execution Date Success is {next_execution_date}')
    return next_execution_date

def calcInterval(ti,**kwargs):
    prevTime,nextTime  = ti.xcom_pull(task_ids=['get_prev_exec','get_next_exec'])   
    print(f'Previous Execution Time is {prevTime}')
    print(f'Next Execution Time is {nextTime}')
    diffTime = nextTime-prevTime
    print(diffTime)
    print(f'Difference Time is {diffTime}')
    
greet_task = BashOperator(
    task_id='greet_task',
    bash_command='echo Hello everyone! Welcome to Python University!',
    dag=dag,
)

get_prev_exec = PythonOperator(
    task_id='get_prev_exec',
    python_callable=getPrevExecutionTime,
    dag=dag,
    provide_context=True
)

get_next_exec = PythonOperator(
    task_id='get_next_exec',
    python_callable=getNextExecutionTime,
    dag=dag,
    provide_context=True
)

calc_interval = PythonOperator(
    task_id='calc_interval',
    python_callable=calcInterval,
    dag=dag,
    provide_context=True
)

greet_task >> [get_prev_exec, get_next_exec] >> calc_interval