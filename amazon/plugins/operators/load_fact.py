from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#80BD9E'
    insert_sql_template='''
        INSERT INTO {table}
        ({select_sql})
    '''

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 table='',
                 select_sql='',
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.select_sql = select_sql

    def execute(self, context):
        self.log.info('LoadFactOperator not implemented yet')
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        formatted_insert = LoadFactOperator \
                           .insert_sql_template \
                           .format(table=self.table,
                                   select_sql=self.select_sql)
        redshift_hook.run(formatted_insert)
