from unittest.mock import patch

import pytest
from parameterized import parameterized

from airflow.models.dag import DAG
from airflow.sensors.date_time import DateTimeSensor
from airflow.utils import timezone

DEFAULT_DATE = timezone.datetime(2015, 1, 1)


class TestDateTimeSensor:
    @classmethod
    def setup_class(cls):
        args = {"owner": "rezaprimasatya", "start_date": DEFAULT_DATE}
        cls.dag = DAG("test_dag", default_args=args)

    @parameterized.expand(
        [
            (
                "valid_datetime",
                timezone.datetime(2020, 7, 6, 13, tzinfo=timezone.utc),
                "2020-07-06T13:00:00+00:00",
            ),
            ("valid_str", "20200706T210000+8", "20200706T210000+8"),
        ]
    )
    def test_valid_input(self, task_id, target_time, expected):
        op = DateTimeSensor(
            task_id=task_id,
            target_time=target_time,
            dag=self.dag,
        )
        assert op.target_time == expected

    def test_invalid_input(self):
        with pytest.raises(TypeError):
            DateTimeSensor(
                task_id="test",
                target_time=timezone.utcnow().time(),
                dag=self.dag,
            )

    @parameterized.expand(
        [
            (
                "poke_datetime",
                timezone.datetime(2020, 1, 1, 22, 59, tzinfo=timezone.utc),
                True,
            ),
            ("poke_str_extended", "2020-01-01T23:00:00.001+00:00", False),
            ("poke_str_basic_with_tz", "20200102T065959+8", True),
        ]
    )
    @patch(
        "airflow.sensors.date_time.timezone.utcnow",
        return_value=timezone.datetime(2020, 1, 1, 23, 0, tzinfo=timezone.utc),
    )
    def test_poke(self, task_id, target_time, expected, mock_utcnow):
        op = DateTimeSensor(task_id=task_id, target_time=target_time, dag=self.dag)
        assert op.poke(None) == expected
