from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries


default_args = {
    'owner': 'cthompson',
    'start_date': datetime(2019, 1, 12, 0),
    'end_date': datetime(2019, 1, 12, 2),
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=300),
    'catchup': False
}

dag = DAG('sparkify_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='@hourly',
          max_active_runs=1
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

create_tables_task = PostgresOperator(
    task_id='Create_tables',
    dag=dag,
    postgres_conn_id='redshift',
    sql='sql/create_tables.sql',
    autocommit=True
)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    table='staging_events',
    s3_bucket='sparkify-data-set',
    s3_key='log_data',
    data_format='json',
    data_option='log_json_path.json'
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    table='staging_songs',
    s3_bucket='sparkify-data-set',
    s3_key='song_data',
    data_format='json'
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='songplays',
    select_sql=SqlQueries.songplay_table_select
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='users',
    select_sql=SqlQueries.user_table_select
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='songs',
    select_sql=SqlQueries.song_table_select
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='artists',
    select_sql=SqlQueries.artist_table_select
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='time',
    select_sql=SqlQueries.time_table_select
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id='redshift',
    tables=['songplays', 'users', 'artists', 'time']
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> create_tables_task >> [stage_events_to_redshift, stage_songs_to_redshift]

load_songplays_table << [stage_events_to_redshift, stage_songs_to_redshift]

load_songplays_table >> [load_song_dimension_table, load_artist_dimension_table,
                         load_user_dimension_table, load_time_dimension_table]

run_quality_checks << [load_song_dimension_table, load_artist_dimension_table,
                       load_user_dimension_table, load_time_dimension_table]

run_quality_checks >> end_operator
