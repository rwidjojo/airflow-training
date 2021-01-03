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

owner = 'efirmant' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(3),
}

dag = DAG(
    f'{owner}.lesson4.excercise6',
    default_args=default_args,
    description='Read data from postgresql',
    schedule_interval=None,
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

def generate_sql(ds):
    return f"""
    SELECT order_date, ship_country, COUNT(order_id) ship_count
    FROM public.recent_orders
    WHERE order_date = '{ds}'
    GROUP BY order_date, ship_country
    ORDER BY order_date
    """

def migrate_odd_day(ds, **kwargs):
    # declare connection
    db_conn = PostgresHook(postgres_conn_id='efirmant_postgres')

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


def migrate_3(ds, **kwargs):
    # declare connection
    db_conn = PostgresHook(postgres_conn_id='efirmant_postgres')

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

def migrate_5(ds, **kwargs):
    # declare connection
    db_conn = PostgresHook(postgres_conn_id='efirmant_postgres')

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


migrate_3 = PythonOperator(
    task_id="migrate_3",
    python_callable=migrate_3,
    provide_context=True,
    dag=dag,
)

migrate_5 = PythonOperator(
    task_id="migrate_5",
    python_callable=migrate_5,
    provide_context=True,
    dag=dag,
)

migrate_odd_task = PythonOperator(
    task_id="migrate_odd",
    python_callable=migrate_odd_day,
    provide_context=True,
    dag=dag,
)

def migrate_even_day(ds, **kwargs):
    # declare connection
    db_conn = PostgresHook(postgres_conn_id='efirmant_postgres')

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
  if execution_date.day % 3 == 0:
    return 'migrate_3' # returning task id `migrate_even_task`
  elif execution_date.day % 2 == 0:
    return 'migrate_even' # returning task id `migrate_even_task`
  else:
    return 'migrate_odd' # returning task id `migrate_odd_task`

def _pick_migrationOdd(**kwargs):
  execution_date = kwargs['execution_date']
  if execution_date.day % 3 == 0:
    return 'migrate_3' # returning task id `migrate_even_task`
  elif execution_date.day % 5 == 0:
    return 'migrate_5' # returning task id `migrate_odd_task`
  else:
    return 'migrate_odd' # returning task id `migrate_odd_task`

migration_branch = BranchPythonOperator(
  task_id='migration_branch',
  provide_context=True,
  python_callable=_pick_migration,
  dag=dag
)

pick_migrationOdd = BranchPythonOperator(
  task_id='pick_migrationOdd',
  provide_context=True,
  python_callable=_pick_migrationOdd,
  dag=dag
)


greet_task >> migration_branch >> [migrate_even_task, migrate_3, migrate_odd_task]

