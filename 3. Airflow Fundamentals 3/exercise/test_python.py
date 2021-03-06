from collections import namedtuple
from datetime import date

from airflow.exceptions import AirflowSensorTimeout
from airflow.sensors.python import PythonSensor
from airflow.utils.state import State
from airflow.utils.timezone import datetime
from airflow.utils.types import DagRunType
from tests.operators.test_python import Call, TestPythonBase, build_recording_function

DEFAULT_DATE = datetime(2015, 1, 1)


class TestPythonSensor(TestPythonBase):
    def test_python_sensor_true(self):
        op = PythonSensor(task_id='python_sensor_check_true', python_callable=lambda: True, dag=self.dag)
        op.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE, ignore_ti_state=True)

    def test_python_sensor_false(self):
        op = PythonSensor(
            task_id='python_sensor_check_false',
            timeout=0.01,
            poke_interval=0.01,
            python_callable=lambda: False,
            dag=self.dag,
        )
        with self.assertRaises(AirflowSensorTimeout):
            op.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE, ignore_ti_state=True)

    def test_python_sensor_raise(self):
        op = PythonSensor(task_id='python_sensor_check_raise', python_callable=lambda: 1 / 0, dag=self.dag)
        with self.assertRaises(ZeroDivisionError):
            op.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE, ignore_ti_state=True)

    def test_python_callable_arguments_are_templatized(self):
        """Test PythonSensor op_args are templatized"""
        recorded_calls = []

        # Create a named tuple and ensure it is still preserved
        # after the rendering is done
        Named = namedtuple('Named', ['var1', 'var2'])
        named_tuple = Named('{{ ds }}', 'unchanged')

        task = PythonSensor(
            task_id='python_sensor',
            timeout=0.01,
            poke_interval=0.3,
            # a Mock instance cannot be used as a callable function or test fails with a
            # TypeError: Object of type Mock is not JSON serializable
            python_callable=build_recording_function(recorded_calls),
            op_args=[4, date(2019, 1, 1), "dag {{dag.dag_id}} ran on {{ds}}.", named_tuple],
            dag=self.dag,
        )

        self.dag.create_dagrun(
            run_type=DagRunType.MANUAL,
            execution_date=DEFAULT_DATE,
            start_date=DEFAULT_DATE,
            state=State.RUNNING,
        )
        with self.assertRaises(AirflowSensorTimeout):
            task.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE)

        ds_templated = DEFAULT_DATE.date().isoformat()
        # 2 calls: first: at start, second: before timeout
        self.assertEqual(2, len(recorded_calls))
        self._assert_calls_equal(
            recorded_calls[0],
            Call(
                4,
                date(2019, 1, 1),
                f"dag {self.dag.dag_id} ran on {ds_templated}.",
                Named(ds_templated, 'unchanged'),
            ),
        )

    def test_python_callable_keyword_arguments_are_templatized(self):
        """Test PythonSensor op_kwargs are templatized"""
        recorded_calls = []

        task = PythonSensor(
            task_id='python_sensor',
            timeout=0.01,
            poke_interval=0.3,
            # a Mock instance cannot be used as a callable function or test fails with a
            # TypeError: Object of type Mock is not JSON serializable
            python_callable=build_recording_function(recorded_calls),
            op_kwargs={
                'an_int': 4,
                'a_date': date(2019, 1, 1),
                'a_templated_string': "dag {{dag.dag_id}} ran on {{ds}}.",
            },
            dag=self.dag,
        )

        self.dag.create_dagrun(
            run_type=DagRunType.MANUAL,
            execution_date=DEFAULT_DATE,
            start_date=DEFAULT_DATE,
            state=State.RUNNING,
        )
        with self.assertRaises(AirflowSensorTimeout):
            task.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE)

        # 2 calls: first: at start, second: before timeout
        self.assertEqual(2, len(recorded_calls))
        self._assert_calls_equal(
            recorded_calls[0],
            Call(
                an_int=4,
                a_date=date(2019, 1, 1),
                a_templated_string="dag {} ran on {}.".format(
                    self.dag.dag_id, DEFAULT_DATE.date().isoformat()
                ),
            ),
        )
