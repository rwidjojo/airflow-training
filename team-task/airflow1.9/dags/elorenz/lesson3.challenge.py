
import logging
from datetime import timedelta

import airflow
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator


owner= 'elorenz'

default_args = {
    'owner': owner,
    'depends_on_past': False,
     'start_date': days_ago(4),
}

dag = DAG(
    #dag_id=f'{owner}.lesson3.challenge',
    dag_id='elorenz.lesson3.challenge',
    default_args=default_args,
    description='DAG challenge pipeline',
    start_date=airflow.utils.dates.days_ago(4),
    schedule_interval= timedelta(days=4),
)

def get_prev_exec(**kwargs):
    prev_exec = kwargs['prev_execution_date']
    logging.info(f"Last execution date= {prev_exec}")
    return prev_exec

def get_next_exec(**kwargs):
    next_exec = kwargs['next_execution_date']
    logging.info(f"Next execution date= {next_exec}")
    return next_exec


def calc_interval(**kwargs):
    ti= kwargs['ti']
    prevexec=ti.xcom_pull(task_ids='get_prev_exec')
    nextexec=ti.xcom_pull(task_ids='get_next_exec')
    intervalday= nextexec -prevexec
    logging.info(f"Result calcuate interval execution time= {intervalday}")
    
gt = BashOperator(
    task_id="greet",
    bash_command='echo "Hello Greeting from Bash Command"',
    dag=dag,
)

t1 = PythonOperator(
    task_id="get_prev_exec",
    python_callable=get_prev_exec,
    #op_args=["prev_execution_date"], jika parsing ini, bakal kirim string value, bukan dari context time runtime
    provide_context=True,
    dag=dag,
)

t2 = PythonOperator(
    task_id="get_next_exec",
    python_callable=get_next_exec,
    #op_args=["next_execution_date"],
    provide_context=True,
    dag=dag,
)

t3 = PythonOperator(
    task_id="calculate",
    python_callable=calc_interval,
    provide_context=True,
    dag=dag,
)

gt >> [t1, t2] >> t3

