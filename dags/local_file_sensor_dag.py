"""Local FileSensor example.

Requires an Airflow connection called fs_default.

In local Astro development, fs_default should point to:
/usr/local/airflow/include/

Create the test file from the project root with:
touch include/data_1.csv

The file can be empty because this DAG only checks whether the file exists.
"""

from airflow.sdk import dag, task
from airflow.providers.standard.sensors.filesystem import FileSensor
from pendulum import datetime


@dag(
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    description="DAG showing how to wait for a local file using a sensor",
    tags=["sensors"],
)
def local_file_sensor_dag():

    wait_for_file = FileSensor(
        task_id="wait_for_file",
        fs_conn_id="fs_default",
        filepath="data_1.csv",
        poke_interval=60,
        mode="reschedule",
    )

    @task
    def process_file():
        print("I processed the local file!")

    wait_for_file >> process_file()


local_file_sensor_dag()
