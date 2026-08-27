from datetime import datetime, timezone

from airflow.sdk import dag, task
from dateutil.relativedelta import relativedelta


@dag(
    dag_id="local_airflow_init_container_example",
    description="A minimal DAG deployed from an init container.",
    schedule="@daily",
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    tags=["example", "local", "init-container"],
)
def local_airflow_init_container_example():
    @task
    def say_hello():
        tomorrow = datetime.now(timezone.utc) + relativedelta(days=1)
        print(
            "Hello from a DAG deployed by an init container! "
            f"Tomorrow is {tomorrow:%Y-%m-%d}."
        )

    say_hello()


@dag(
    dag_id="local_airflow_init_container_example_2",
    description="A minimal DAG deployed from an init container 2.",
    schedule="@daily",
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    tags=["example", "local", "init-container"],
)
def local_airflow_init_container_example_2():
    @task
    def say_hello():
        tomorrow = datetime.now(timezone.utc) + relativedelta(days=1)
        print(
            "Hello from a DAG deployed by an init container! "
            f"Tomorrow is {tomorrow:%Y-%m-%d}."
        )

    say_hello()

local_airflow_init_container_example()
local_airflow_init_container_example_2()
