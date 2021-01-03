import airflow
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.models import Variable

vOwn = Variable.get("owner_paulusindra", deserialize_json=True)

owner = vOwn["name"] # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

dag = DAG(
  dag_id=f'{owner}.lesson3.excercise6',
  start_date=airflow.utils.dates.days_ago(3),
  schedule_interval=None,
)

print_template =  BashOperator(
    task_id="print_template",
    bash_command='echo "execution date is {{ ts }} with year {{ execution_date.year }} and month {{ \'{:02}\'.format(execution_date.month) }}"',
    dag=dag,
)