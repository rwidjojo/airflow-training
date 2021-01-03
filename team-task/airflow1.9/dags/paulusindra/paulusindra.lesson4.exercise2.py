# Instruction 
# refactor DAG below so SQL script could query data incrementally

from datetime import timedelta
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable

vOwn = Variable.get("owner_paulusindra", deserialize_json=True)

owner = vOwn["name"] # Replace with your short name

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': days_ago(3),
}

dag = DAG(
    f'{owner}.lesson4.exercise2',
    default_args=default_args,
    description='Read data from postgresql',
    schedule_interval=None,
)

def migrate_data(ds, **kwargs):
    # declare connection
    db_conn = PostgresHook(postgres_conn_id='paulusindra_postgres')

    # declare sql string
    read_sql = f"""
    SELECT order_date, ship_country, COUNT(order_id) ship_count
    FROM public.recent_orders
    WHERE order_date = '{ds}'
    GROUP BY order_date, ship_country
    ORDER BY order_date
    """

    # execute sql
    insert_sql = """
        insert into public.shipping_count(
            order_date
            , ship_country
            , ship_count)
        values(%s, %s, %s)
        on conflict(
            order_date
            , ship_country
        )
        do nothing;
    """
    
    # log formatted sql so it easier to debug
    logging.info(read_sql)

    result = db_conn.get_records(read_sql)

    for row in result:
        logging.info(row)

    for row in result:
        logging.info(insert_sql)
        db_conn.run(
            insert_sql
            , parameters=(
                row['order_date'],
                row['ship_country'],
                row['ship_count']
                )
        )

migrate = PythonOperator(
    task_id="migrate",
    python_callable=migrate_data,
    provide_context=True,
    dag=dag
)

