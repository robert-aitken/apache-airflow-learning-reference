from airflow.sdk import dag, task
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from pendulum import datetime


@dag(
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    description="DAG showing how to wait for a file in S3 using a sensor",
    tags=["sensors"],
)
def sensors_dag():

    wait_for_file = S3KeySensor(
        task_id="wait_for_file",
        aws_conn_id="aws_s3",
        bucket_key="s3://example-bucket/data_*",
        wildcard_match=True,
        mode="reschedule",
    )

    @task
    def process_file():
        print("I processed the file!")

    wait_for_file >> process_file()


sensors_dag()
