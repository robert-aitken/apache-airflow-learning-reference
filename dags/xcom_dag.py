# Share the value from task_a to task_b using XCom.
from airflow.sdk import dag, task


@dag
def xcom_dag():

    @task
    def task_a():
        val = 42
        return val

    @task
    def task_b(val: int):
        print(val)

    val = task_a()
    task_b(val)


xcom_dag()
