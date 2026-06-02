from airflow.sdk import dag, task
from airflow.sensors.base import PokeReturnValue
from pendulum import datetime
import requests


@dag(
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    description="DAG showing how to use a custom API sensor",
    tags=["sensors"],
)
def api_custom_sensor_dag():

    @task.sensor(poke_interval=30, timeout=3600, mode="reschedule")
    def check_api_available() -> PokeReturnValue:
        response = requests.get(
            "https://jsonplaceholder.typicode.com/todos/1", timeout=10
        )
        print(response.status_code)

        if response.status_code == 200:
            condition_met = True
            operator_return_value = response.json()
        else:
            condition_met = False
            operator_return_value = None
            print(f"API returned status code {response.status_code}")

        return PokeReturnValue(
            is_done=condition_met,
            xcom_value=operator_return_value,
        )

    @task
    def print_todo(todo: dict):
        print(todo)

    print_todo(check_api_available())


api_custom_sensor_dag()
