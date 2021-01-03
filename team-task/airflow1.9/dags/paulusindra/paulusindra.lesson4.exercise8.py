# Instruction 
# Try run this DAG

from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable

vOwn = Variable.get('owner_paulusindra', deserialize_json=True)

owner = vOwn['name'] # Replace with your short name
# declare connection
db_conn = PostgresHook(postgres_conn_id='paulusindra_postgres')

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(3),
}

dag = DAG(
    f'{owner}.lesson4.exercise8',
    default_args=default_args,
    description='Read data from postgresql',
    schedule_interval='@daily',
)

greet_task = BashOperator(
    task_id="greet",
    bash_command=f'echo "Hello {owner}"',
    dag=dag,
)


# declare insert sql
insert_sql = """
INSERT INTO public.shipping_count(order_date, ship_country, ship_count)
VALUES(%s, %s, %s)
ON CONFLICT (order_date, ship_country)
DO NOTHING;
"""

def generate_sql(ds,x):
    y=2
    if x:
        y=1
    print(f'Multiplier is {y}')
    return f"""
    SELECT order_date, ship_country, COUNT(order_id)*{y} ship_count
    FROM public.recent_orders
    WHERE order_date = '{ds}'
    GROUP BY order_date, ship_country
    ORDER BY order_date
    """

def migrate_odd_day(ds, **kwargs):

    # declare sql string
    sql = generate_sql(ds,True)

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
    sql = generate_sql(ds,True)

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
    return 'migrate_even' # returning task id `migrate_even_task`
  else:
    return 'migrate_odd' # returning task id `migrate_odd_task`


migration_branch = BranchPythonOperator(
  task_id='migration_branch',
  provide_context=True,
  python_callable=_pick_migration,
  dag=dag
)

def _check_row_task(ds, **kwargs):
    read_sql = f"""
        SELECT COUNT(*) as count_row
        FROM public.recent_orders
        WHERE order_date = '{ds}'
        """

    result = db_conn.get_records(read_sql)

    for row in result:
        print(f'Record inserted {ds} is {row} rows')

check_row_task = PythonOperator(
    task_id='check_row_task',
    provide_context=True,
    python_callable=_check_row_task,
    dag=dag,
    trigger_rule="none_failed",
)


greet_task >> migration_branch >> [migrate_even_task, migrate_odd_task] >> check_row_task