import unittest
from datetime import timedelta

from airflow.models import DagBag
from airflow.models.dag import DAG
from airflow.sensors.time_delta import TimeDeltaSensor
from airflow.utils.timezone import datetime

DEFAULT_DATE = datetime(2015, 1, 1)
DEV_NULL = '/dev/null'
TEST_DAG_ID = 'unit_tests'


class TestTimedeltaSensor(unittest.TestCase):
    def setUp(self):
        self.dagbag = DagBag(dag_folder=DEV_NULL, include_examples=True)
        self.args = {'owner': 'airflow', 'start_date': DEFAULT_DATE}
        self.dag = DAG(TEST_DAG_ID, default_args=self.args)

    def test_timedelta_sensor(self):
        op = TimeDeltaSensor(task_id='timedelta_sensor_check', delta=timedelta(seconds=2), dag=self.dag)
        op.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE, ignore_ti_state=True)
