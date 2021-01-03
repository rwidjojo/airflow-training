# Instruction 
# create new task to check migrate_even_day run
# only if execution date is even but 
# not multiplication of 4 like 4, 8, 12, etc

from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable
from airflow.exceptions import AirflowSkipException

ownerJSON = Variable.get("owner_rwidjojo", deserialize_json=True) # Replace with your short name

owner = ownerJSON["name"]

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(3),
}

dag = DAG(
    f'{owner}.lesson4.excercise7',
    default_args=default_args,
    description='Read data from postgresql',
    schedule_interval="@daily",
)

greet_task = BashOperator(
    task_id="greet",
    bash_command=f'echo "Hello {owner}"',
    dag=dag,
)

# declare connection
db_conn = PostgresHook(postgres_conn_id='rwidjojo_postgres')

# declare insert sql
insert_sql = """
INSERT INTO public.shipping_count(order_date, ship_country, ship_count)
VALUES(%s, %s, %s)
ON CONFLICT (order_date, ship_country)
DO NOTHING;
"""

def generate_sql(ds):
    return f"""
    SELECT order_date, ship_country, COUNT(order_id) ship_count
    FROM public.recent_orders
    WHERE order_date = '{ds}'
    GROUP BY order_date, ship_country
    ORDER BY order_date
    """

def migrate_odd_day(ds, **kwargs):

    # declare sql string
    sql = generate_sql(ds)

    # log formatted sql so it easier to debug
    logging.info(sql)

    # execute sql
    result = db_conn.get_records(sql)

    # insert each row to table `public.shipping_count`
    for row in result:
        db_conn.run(
        insert_sql,
        parameters=(
            row['order_date'],
            row['ship_country'],
            row['ship_count'])
        )

migrate_odd_task = PythonOperator(
    task_id="migrate_odd",
    python_callable=migrate_odd_day,
    provide_context=True,
    dag=dag,
)

def migrate_even_day(ds, **kwargs):

    # declare sql string
    sql = generate_sql(ds)

    # log formatted sql so it easier to debug
    logging.info(sql)

    # execute sql
    result = db_conn.get_records(sql)

    # insert each row to table `public.shipping_count`
    for row in result:
        db_conn.run(
        insert_sql,
        parameters=(
            row['order_date'],
            row['ship_country'],
            row['ship_count'])
        )

migrate_even_task = PythonOperator(
    task_id="migrate_even",
    python_callable=migrate_even_day,
    provide_context=True,
    dag=dag,
)

def _pick_migration(**kwargs):
  execution_date = kwargs['execution_date']
  if execution_date.day % 2 == 0:
    return 'checker_fourth' # returning task id `checker_fourth`
  else:
    return 'migrate_odd' # returning task id `migrate_odd_task`

migration_branch = BranchPythonOperator(
  task_id='migration_branch',
  provide_context=True,
  python_callable=_pick_migration,
  dag=dag
)

def every_fourth(**context):
    # Find the boundaries for our execution window.
    myvar = context['execution_date']
    if myvar.day % 4 != 0:
        print(f"Next job should run, since today is {myvar.day}")
    else:
        raise AirflowSkipException("Skipping because the date is divisible by four")

checker_fourth = PythonOperator(
  task_id='checker_fourth',
  provide_context=True,
  python_callable=every_fourth,
  dag=dag
)   

greet_task >> migration_branch >> [checker_fourth, migrate_odd_task]
checker_fourth >> migrate_even_task