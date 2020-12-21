import os
import unittest
from unittest import mock

import pytest

from airflow.exceptions import AirflowException
from airflow.models.dag import DAG
from airflow.sensors.sql import SqlSensor
from airflow.utils.timezone import datetime
from tests.providers.apache.hive import TestHiveEnvironment

DEFAULT_DATE = datetime(2015, 1, 1)
TEST_DAG_ID = 'unit_test_sql_dag'


class TestSqlSensor(TestHiveEnvironment):
    def setUp(self):
        super().setUp()
        args = {'owner': 'airflow', 'start_date': DEFAULT_DATE}
        self.dag = DAG(TEST_DAG_ID, default_args=args)

    def test_unsupported_conn_type(self):
        op = SqlSensor(
            task_id='sql_sensor_check',
            conn_id='redis_default',
            sql="SELECT count(1) FROM INFORMATION_SCHEMA.TABLES",
            dag=self.dag,
        )

        with self.assertRaises(AirflowException):
            op.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE, ignore_ti_state=True)

    @pytest.mark.backend("mysql")
    def test_sql_sensor_mysql(self):
        op1 = SqlSensor(
            task_id='sql_sensor_check_1',
            conn_id='mysql_default',
            sql="SELECT count(1) FROM INFORMATION_SCHEMA.TABLES",
            dag=self.dag,
        )
        op1.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE, ignore_ti_state=True)

        op2 = SqlSensor(
            task_id='sql_sensor_check_2',
            conn_id='mysql_default',
            sql="SELECT count(%s) FROM INFORMATION_SCHEMA.TABLES",
            parameters=["table_name"],
            dag=self.dag,
        )
        op2.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE, ignore_ti_state=True)

    @pytest.mark.backend("postgres")
    def test_sql_sensor_postgres(self):
        op1 = SqlSensor(
            task_id='sql_sensor_check_1',
            conn_id='postgres_default',
            sql="SELECT count(1) FROM INFORMATION_SCHEMA.TABLES",
            dag=self.dag,
        )
        op1.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE, ignore_ti_state=True)

        op2 = SqlSensor(
            task_id='sql_sensor_check_2',
            conn_id='postgres_default',
            sql="SELECT count(%s) FROM INFORMATION_SCHEMA.TABLES",
            parameters=["table_name"],
            dag=self.dag,
        )
        op2.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE, ignore_ti_state=True)

    @mock.patch('airflow.sensors.sql.BaseHook')
    def test_sql_sensor_postgres_poke(self, mock_hook):
        op = SqlSensor(
            task_id='sql_sensor_check',
            conn_id='postgres_default',
            sql="SELECT 1",
        )

        mock_hook.get_connection('postgres_default').conn_type = "postgres"
        mock_get_records = mock_hook.get_connection.return_value.get_hook.return_value.get_records

        mock_get_records.return_value = []
        self.assertFalse(op.poke(None))

        mock_get_records.return_value = [[None]]
        self.assertFalse(op.poke(None))

        mock_get_records.return_value = [['None']]
        self.assertTrue(op.poke(None))

        mock_get_records.return_value = [[0.0]]
        self.assertFalse(op.poke(None))

        mock_get_records.return_value = [[0]]
        self.assertFalse(op.poke(None))

        mock_get_records.return_value = [['0']]
        self.assertTrue(op.poke(None))

        mock_get_records.return_value = [['1']]
        self.assertTrue(op.poke(None))

    @mock.patch('airflow.sensors.sql.BaseHook')
    def test_sql_sensor_postgres_poke_fail_on_empty(self, mock_hook):
        op = SqlSensor(
            task_id='sql_sensor_check', conn_id='postgres_default', sql="SELECT 1", fail_on_empty=True
        )

        mock_hook.get_connection('postgres_default').conn_type = "postgres"
        mock_get_records = mock_hook.get_connection.return_value.get_hook.return_value.get_records

        mock_get_records.return_value = []
        self.assertRaises(AirflowException, op.poke, None)

    @mock.patch('airflow.sensors.sql.BaseHook')
    def test_sql_sensor_postgres_poke_success(self, mock_hook):
        op = SqlSensor(
            task_id='sql_sensor_check', conn_id='postgres_default', sql="SELECT 1", success=lambda x: x in [1]
        )

        mock_hook.get_connection('postgres_default').conn_type = "postgres"
        mock_get_records = mock_hook.get_connection.return_value.get_hook.return_value.get_records

        mock_get_records.return_value = []
        self.assertFalse(op.poke(None))

        mock_get_records.return_value = [[1]]
        self.assertTrue(op.poke(None))

        mock_get_records.return_value = [['1']]
        self.assertFalse(op.poke(None))

    @mock.patch('airflow.sensors.sql.BaseHook')
    def test_sql_sensor_postgres_poke_failure(self, mock_hook):
        op = SqlSensor(
            task_id='sql_sensor_check', conn_id='postgres_default', sql="SELECT 1", failure=lambda x: x in [1]
        )

        mock_hook.get_connection('postgres_default').conn_type = "postgres"
        mock_get_records = mock_hook.get_connection.return_value.get_hook.return_value.get_records

        mock_get_records.return_value = []
        self.assertFalse(op.poke(None))

        mock_get_records.return_value = [[1]]
        self.assertRaises(AirflowException, op.poke, None)

    @mock.patch('airflow.sensors.sql.BaseHook')
    def test_sql_sensor_postgres_poke_failure_success(self, mock_hook):
        op = SqlSensor(
            task_id='sql_sensor_check',
            conn_id='postgres_default',
            sql="SELECT 1",
            failure=lambda x: x in [1],
            success=lambda x: x in [2],
        )

        mock_hook.get_connection('postgres_default').conn_type = "postgres"
        mock_get_records = mock_hook.get_connection.return_value.get_hook.return_value.get_records

        mock_get_records.return_value = []
        self.assertFalse(op.poke(None))

        mock_get_records.return_value = [[1]]
        self.assertRaises(AirflowException, op.poke, None)

        mock_get_records.return_value = [[2]]
        self.assertTrue(op.poke(None))

    @mock.patch('airflow.sensors.sql.BaseHook')
    def test_sql_sensor_postgres_poke_failure_success_same(self, mock_hook):
        op = SqlSensor(
            task_id='sql_sensor_check',
            conn_id='postgres_default',
            sql="SELECT 1",
            failure=lambda x: x in [1],
            success=lambda x: x in [1],
        )

        mock_hook.get_connection('postgres_default').conn_type = "postgres"
        mock_get_records = mock_hook.get_connection.return_value.get_hook.return_value.get_records

        mock_get_records.return_value = []
        self.assertFalse(op.poke(None))

        mock_get_records.return_value = [[1]]
        self.assertRaises(AirflowException, op.poke, None)

    @mock.patch('airflow.sensors.sql.BaseHook')
    def test_sql_sensor_postgres_poke_invalid_failure(self, mock_hook):
        op = SqlSensor(
            task_id='sql_sensor_check',
            conn_id='postgres_default',
            sql="SELECT 1",
            failure=[1],
        )

        mock_hook.get_connection('postgres_default').conn_type = "postgres"
        mock_get_records = mock_hook.get_connection.return_value.get_hook.return_value.get_records

        mock_get_records.return_value = [[1]]
        with self.assertRaises(AirflowException) as e:
            op.poke(None)
        self.assertEqual("self.failure is present, but not callable -> [1]", str(e.exception))

    @mock.patch('airflow.sensors.sql.BaseHook')
    def test_sql_sensor_postgres_poke_invalid_success(self, mock_hook):
        op = SqlSensor(
            task_id='sql_sensor_check',
            conn_id='postgres_default',
            sql="SELECT 1",
            success=[1],
        )

        mock_hook.get_connection('postgres_default').conn_type = "postgres"
        mock_get_records = mock_hook.get_connection.return_value.get_hook.return_value.get_records

        mock_get_records.return_value = [[1]]
        with self.assertRaises(AirflowException) as e:
            op.poke(None)
        self.assertEqual("self.success is present, but not callable -> [1]", str(e.exception))

    @unittest.skipIf(
        'AIRFLOW_RUNALL_TESTS' not in os.environ, "Skipped because AIRFLOW_RUNALL_TESTS is not set"
    )
    def test_sql_sensor_presto(self):
        op = SqlSensor(
            task_id='hdfs_sensor_check',
            conn_id='presto_default',
            sql="SELECT 'x' FROM airflow.static_babynames LIMIT 1;",
            dag=self.dag,
        )
        op.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE, ignore_ti_state=True)
