# Instruction 
# Try run this DAG


from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

owner = 'dtjayain' # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(3),
}

dag = DAG(
    f'{owner}.lesson4.excercise4',
    default_args=default_args,
    description='Read data from postgresql',
    schedule_interval="@daily",
)

# declare insert sql
insert_sql = """
INSERT INTO public.shipping_count(order_date, ship_country, ship_count)
VALUES(%s, %s, %s)
ON CONFLICT (order_date, ship_country)
DO NOTHING;
"""

# declare connection
db_conn = PostgresHook(postgres_conn_id='dtjayain_postgress')

def generate_sql(ds, is_odd):
    multiplier = 1
    if not is_odd:
        multiplier = 2
    return f"""
    SELECT order_date, ship_country, COUNT(order_id) * {multiplier} ship_count
    FROM public.recent_orders
    WHERE order_date = '{ds}'
    GROUP BY order_date, ship_country
    ORDER BY order_date
    """

def migrate_odd_day(ds, **kwargs):

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

def migrate_even_day(ds, **kwargs):

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


def migrate_data(**kwargs):
  execution_date = kwargs['execution_date']
  if execution_date.day % 2 == 0:
    migrate_even_day(**kwargs)
  else:
    migrate_odd_day(**kwargs)


migrate_task = PythonOperator(
    task_id="migrate",
    python_callable=migrate_data,
    provide_context=True,
    dag=dag,
)