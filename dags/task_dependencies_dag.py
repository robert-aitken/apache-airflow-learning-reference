from airflow.sdk import chain, dag, task
from pendulum import datetime

default_args = {
    "retries": 3,
}


@dag(
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    description="DAG showing task dependencies with chain",
    tags=["team_a", "source_a"],
    max_consecutive_failed_dag_runs=3,
    default_args=default_args,
)
def task_dependencies_dag():

    @task
    def task_a():
        print("Hello from task A!")

    @task
    def task_b():
        print("Hello from task B!")

    @task
    def task_c():
        print("Hello from task C!")

    @task
    def task_d():
        print("Hello from task D!")

    @task
    def task_e():
        print("Hello from task E!")

    # Basic chain:
    # task_a -> task_b
    # task_a() >> task_b()

    # Fan-out after task_b:
    # task_a -> task_b -> task_c
    #                  \
    #                   task_d
    # task_a() >> task_b() >> [task_c(), task_d()]

    # Branching chain using chain:
    #        task_b -> task_c
    #       /
    # task_a
    #       \
    #        task_d -> task_e
    chain(task_a(), [task_b(), task_d()], [task_c(), task_e()])

    # Same branching chain without chain:
    # a = task_a()
    # a >> task_b() >> task_c()
    # a >> task_d() >> task_e()


task_dependencies_dag()
