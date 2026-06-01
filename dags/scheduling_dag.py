from airflow.sdk import dag, task
from pendulum import datetime

# Cron schedule:
# 0 5 * * 1,3,5
# Minute: 0
# Hour: 5
# Day of month: any
# Month: any
# Day of week: Monday, Wednesday, Friday


@dag(
    schedule="0 5 * * 1,3,5",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    description="DAG showing Monday, Wednesday, and Friday scheduling at 5 AM",
    tags=["scheduling"],
)
def scheduling_dag():

    @task
    def task_a():
        print("This DAG can be scheduled from 2025-01-01.")

    @task
    def task_b():
        print("This DAG runs every Monday, Wednesday, and Friday at 5 AM.")

    @task
    def task_c():
        print("With catchup=False, only the latest missing run is created.")

    task_a() >> task_b() >> task_c()


scheduling_dag()
