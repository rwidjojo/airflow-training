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
from airflow.exceptions import AirflowSkipException

owner = 'msantoso4' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(5),
}

dag = DAG(
    f'{owner}.lesson4.excercise7',
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

def generate_sql(ds, is_odd):
    multiplier = 1
    if not is_odd:
        multiplier = 2
    return f"""
    SELECT order_date, ship_country, (COUNT(order_id) * {multiplier}) ship_count
    FROM public.recent_orders
    WHERE order_date = '{ds}'
    GROUP BY order_date, ship_country
    ORDER BY order_date
    """

def migrate_odd_day(ds, **kwargs):
    # declare connection
    db_conn = PostgresHook(postgres_conn_id='msantoso4_postgree')

    # declare sql string
    sql = generate_sql(ds, True)

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
    # declare connection
    db_conn = PostgresHook(postgres_conn_id='msantoso4_postgree')

    # declare sql string
    sql = generate_sql(ds, False)

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
    return 'check_4_multiplier' # returning task id `migrate_even_task`
  else:
    return 'migrate_odd' # returning task id `migrate_odd_task`


migration_branch = BranchPythonOperator(
  task_id='migration_branch',
  provide_context=True,
  python_callable=_pick_migration,
  dag=dag
)

def _is_multiplied_by_4(**kwargs):
  execution_date = kwargs['execution_date']
  if execution_date.day % 4 == 0:
    raise AirflowSkipException("Multiplied by 4")
  


is_multiplied_by_4 = PythonOperator(
  task_id="check_4_multiplier",
  python_callable=_is_multiplied_by_4,
  provide_context=True,
  dag=dag,
)


greet_task >> migration_branch >> [is_multiplied_by_4, migrate_odd_task]

is_multiplied_by_4 >> migrate_even_task