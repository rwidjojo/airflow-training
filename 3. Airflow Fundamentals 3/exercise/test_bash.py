import datetime
import unittest

from airflow.exceptions import AirflowSensorTimeout
from airflow.models.dag import DAG
from airflow.sensors.bash import BashSensor


class TestBashSensor(unittest.TestCase):
    def setUp(self):
        args = {'owner': 'airflow', 'start_date': datetime.datetime(2017, 1, 1)}
        dag = DAG('test_dag_id', default_args=args)
        self.dag = dag

    def test_true_condition(self):
        op = BashSensor(
            task_id='test_true_condition',
            bash_command='freturn() { return "$1"; }; freturn 0',
            output_encoding='utf-8',
            poke_interval=1,
            timeout=2,
            dag=self.dag,
        )
        op.execute(None)

    def test_false_condition(self):
        op = BashSensor(
            task_id='test_false_condition',
            bash_command='freturn() { return "$1"; }; freturn 1',
            output_encoding='utf-8',
            poke_interval=1,
            timeout=2,
            dag=self.dag,
        )
        with self.assertRaises(AirflowSensorTimeout):
            op.execute(None)
