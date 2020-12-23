from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    copy_sql_template = """
        COPY {table} 
        FROM '{s3_path}'    
        ACCESS_KEY_ID '{access_key}'
        SECRET_ACCESS_KEY '{secret_key}'
        FORMAT AS {data_format} '{data_option}'
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 aws_credentials_id='',
                 table='',
                 s3_bucket='',
                 s3_key='',
                 data_format='',
                 data_option='auto',
                 time_format='epochmillisecs',
                 accept_inv_chars='^',
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)

        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.data_format = data_format
        self.data_option = data_option

    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        s3_path = "s3://{}/{}".format(self.s3_bucket, self.s3_key)
        
        if self.data_option != 'auto':
            self.data_option = "s3://{}/{}".format(self.s3_bucket, self.data_option)
        
        formatted_sql = StageToRedshiftOperator.copy_sql_template.format(
            table=self.table,
            s3_path=s3_path,
            access_key=credentials.access_key,
            secret_key=credentials.secret_key,
            data_format=self.data_format,
            data_option=self.data_option)
        
        self.log.info("Clearing data from destination Redshift table")
        redshift.run("DELETE FROM {}".format(self.table))
        redshift.run(formatted_sql)
        
            
        




