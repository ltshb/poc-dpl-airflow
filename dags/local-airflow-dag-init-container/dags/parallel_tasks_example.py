from datetime import datetime, timezone

from airflow.sdk import dag, task


@dag(
    dag_id="parallel_tasks_example",
    description="An example DAG that fans out into two parallel tasks.",
    schedule="@daily",
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    tags=["example", "local", "init-container", "parallel"],
)
def parallel_tasks_example():
    @task
    def first_task():
        print("The first task has completed.")

    @task
    def parallel_task_one():
        print("The first parallel task has completed.")

    @task
    def parallel_task_two():
        print("The second parallel task has completed.")

    first = first_task()
    first >> [parallel_task_one(), parallel_task_two()]


parallel_tasks_example()
