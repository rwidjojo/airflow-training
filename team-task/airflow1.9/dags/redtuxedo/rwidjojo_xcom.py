from __future__ import print_function
from pprint import pprint
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable

owner = Variable.get("owner_rwidjojo", deserialize_json=True)

args = {
    'owner': owner["name"],
    'start_date': airflow.utils.dates.days_ago(2),
    'provide_context': True
}

dag = DAG(
    f'{owner["name"]}_example_xcom',
    schedule_interval="@once",
    default_args=args)

value_1 = [1, 2, 3]
value_2 = {'a': 'b'}


def push(**kwargs):
    # pushes an XCom without a specific target
    kwargs['ti'].xcom_push(key='value from pusher 1', value=value_1)

def push_by_returning(**kwargs):
    # pushes an XCom without a specific target, just by returning it
    return value_2


def puller(**kwargs):
    ti = kwargs['ti']

    # get value_1
    v1 = ti.xcom_pull(key=None, task_ids='push')
    assert v1 == value_1

    # get value_2
    v2 = ti.xcom_pull(task_ids='push_by_returning')
    assert v2 == value_2

    # get both value_1 and value_2
    v1, v2 = ti.xcom_pull(key=None, task_ids=['push', 'push_by_returning'])
    assert (v1, v2) == (value_1, value_2)

def printing(**kwargs):
    pprint(kwargs)

push1 = PythonOperator(
    task_id='push', dag=dag, python_callable=push)

push2 = PythonOperator(
    task_id='push_by_returning', dag=dag, python_callable=push_by_returning)

pull = PythonOperator(
    task_id='puller', dag=dag, python_callable=puller)

printer = PythonOperator(
    task_id='printer', dag=dag, python_callable=printing, provide_context=False)

[push1, push2] >> pull >> printer