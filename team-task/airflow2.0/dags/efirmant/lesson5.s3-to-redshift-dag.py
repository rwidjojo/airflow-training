import datetime
import logging

from airflow import DAG
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator

import sql_statements


def load_data_to_redshift(*args, **kwargs):
    # use AWS hook to get to aws connection id
    aws_hook = AwsHook("aws_credentials", client_type="s3")
    credentials = aws_hook.get_credentials()
    
    # use PostgresHook to get to redshift connection id
    redshift_hook = PostgresHook("efirmant_redshift")
    redshift_hook.run(sql_statements.COPY_ALL_TRIPS_SQL.format(credentials.access_key, credentials.secret_key))

# default arguments for each task
default_args = {
    'owner': 'efirmant',
}

owner = 'efirmant'

dag = DAG(
    f'{owner}.lesson5.s3-to-redshift-dag',
    start_date=datetime.datetime.now()
)

create_table = PostgresOperator(
    task_id="create_table",
    dag=dag,
    postgres_conn_id="efirmant_redshift",
    sql=sql_statements.CREATE_TRIPS_TABLE_SQL
)

copy_task = PythonOperator(
    task_id='load_from_s3_to_redshift',
    dag=dag,
    python_callable=load_data_to_redshift
)

location_traffic_task = PostgresOperator(
    task_id="calculate_location_traffic",
    dag=dag,
    postgres_conn_id="efirmant_redshift",
    sql=sql_statements.LOCATION_TRAFFIC_SQL
)

create_table >> copy_task
copy_task >> location_traffic_task