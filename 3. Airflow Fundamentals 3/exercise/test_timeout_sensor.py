import time
import unittest
from datetime import timedelta

from airflow.exceptions import AirflowSensorTimeout, AirflowSkipException
from airflow.models.dag import DAG
from airflow.sensors.base import BaseSensorOperator
from airflow.utils import timezone
from airflow.utils.decorators import apply_defaults
from airflow.utils.timezone import datetime

DEFAULT_DATE = datetime(2015, 1, 1)
TEST_DAG_ID = 'unit_test_dag'


class TimeoutTestSensor(BaseSensorOperator):
    @apply_defaults
    def __init__(self, return_value=False, **kwargs):
        self.return_value = return_value
        super().__init__(**kwargs)

    def poke(self, context):
        return self.return_value

    def execute(self, context):
        started_at = timezone.utcnow()
        time_jump = self.params.get('time_jump')
        while not self.poke(context):
            if time_jump:
                started_at -= time_jump
            if (timezone.utcnow() - started_at).total_seconds() > self.timeout:
                if self.soft_fail:
                    raise AirflowSkipException('Snap. Time is OUT.')
                else:
                    raise AirflowSensorTimeout('Snap. Time is OUT.')
            time.sleep(self.poke_interval)
        self.log.info("Success criteria met. Exiting.")


class TestSensorTimeout(unittest.TestCase):
    def setUp(self):
        args = {'owner': 'airflow', 'start_date': DEFAULT_DATE}
        self.dag = DAG(TEST_DAG_ID, default_args=args)

    def test_timeout(self):
        op = TimeoutTestSensor(
            task_id='test_timeout',
            execution_timeout=timedelta(days=2),
            return_value=False,
            poke_interval=5,
            params={'time_jump': timedelta(days=2, seconds=1)},
            dag=self.dag,
        )
        self.assertRaises(
            AirflowSensorTimeout, op.run, start_date=DEFAULT_DATE, end_date=DEFAULT_DATE, ignore_ti_state=True
        )
