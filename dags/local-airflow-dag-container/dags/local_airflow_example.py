from airflow.sdk import dag, task
from dateutil.parser import isoparse


@dag(
    dag_id="local_airflow_example",
    description="A minimal Dag baked into the Airflow Docker image.",
    schedule="@daily",
    start_date=isoparse("2026-01-01T00:00:00Z"),
    catchup=False,
    tags=["example", "local"],
)
def local_airflow_example():
    @task
    def say_hello():
        print("Hello from a Dag baked into the Airflow image!")

    say_hello()


local_airflow_example()
