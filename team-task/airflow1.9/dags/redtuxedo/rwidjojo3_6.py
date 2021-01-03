import airflow
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.models import Variable

ownerJSON = Variable.get("owner_rwidjojo", deserialize_json=True) # Replace with your short name

owner = ownerJSON["name"]

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(2),
}

def myfunc(**kwargs):
    myvar = kwargs["ds"]
    print(f"Now is {var}")

dag = DAG(
  dag_id=f'{owner}.lesson3.excercise6',
  start_date=airflow.utils.dates.days_ago(3),
  schedule_interval=None,
  default_args=default_args
)

print_template =  BashOperator(
    task_id="print_template",
    bash_command='echo "execution date is {{ ts }} with year {{ execution_date.year }} and month {{ \'{:02}\'.format(execution_date.month) }}"',
    dag=dag,
)

print_template_2 =  BashOperator(
    task_id="print_template_2",
    bash_command='echo "execution date is {{ts}} with year {{execution_date.year}} and month {{ \'{:02}\'.format(execution_date.month) }}"',
    dag=dag,
)

printing = PythonOperator(
  task_id="printing",
  python_callable=myfunc,
  provide_context=True,
  dag=dag,
)

print_template >> print_template_2 >> printing