from airflow.sdk import dag, task, Variable
from pendulum import datetime


@dag(
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    description="DAG showing how to read an Airflow variable",
    tags=["variables"],
)
def variable_dag():

    @task
    def print_api_config():
        api_config = Variable.get("api", deserialize_json=True)
        print(api_config)

    print_api_config()


variable_dag()
