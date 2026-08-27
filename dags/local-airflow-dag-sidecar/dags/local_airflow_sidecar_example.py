from datetime import datetime, timezone

from airflow.sdk import dag, task


@dag(
    dag_id="local_airflow_sidecar_example",
    description="A minimal DAG deployed from a sidecar container.",
    schedule="@daily",
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    tags=["example", "local", "sidecar"],
)
def local_airflow_sidecar_example():
    @task
    def say_hello():
        print("Hello from a DAG deployed by a sidecar container!")

    say_hello()


local_airflow_sidecar_example()
