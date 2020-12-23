from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'
    truncate_sql_template='''TRUNCATE {table}'''
    insert_sql_template='''
        INSERT INTO {table}
        ({select_sql})
    '''

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 table='',
                 select_sql='',
                 truncate_before_insert=False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.select_sql = select_sql
        self.truncate_before_insert = truncate_before_insert

    def execute(self, context):
        self.log.info('LoadDimensionOperator not implemented yet')
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if self.truncate_before_insert:
            formatted_truncate = LoadDimensionOperator \
                                .truncate_sql_template \
                                .format(table=self.table)
            redshift_hook.run(formatted_truncate)

        formatted_insert = LoadDimensionOperator \
                           .insert_sql_template \
                           .format(table=self.table,
                                   select_sql=self.select_sql)
        redshift_hook.run(formatted_insert)
