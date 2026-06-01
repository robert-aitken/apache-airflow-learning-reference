# Share multiple values between tasks using XCom.
from airflow.sdk import dag, task


@dag
def xcom_dag():

    @task
    def task_a():
        values = {
            "val_1": 42,
            "val_2": 43,
        }
        return values

    @task
    def task_b(values: dict):
        print(values)

    values = task_a()
    task_b(values)


xcom_dag()
