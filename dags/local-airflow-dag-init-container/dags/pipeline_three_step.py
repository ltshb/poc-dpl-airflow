import logging

from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG
from airflow.sdk.definitions.param import Param, ParamsDict
from pipeline_tooling.from_nodes import apply_nodes, generate_node_tree
from pipeline_tooling.importer import download_from_s3
from pipeline_tooling.reader import parse_yaml

logger = logging.getLogger("pipeline_three_step")

# Define default arguments for the DAG
default_args = {"owner": "airflow", "depends_on_past": False, "retries": 0}

# Create the DAG
dag = DAG(
    "three_step_pipeline",
    default_args=default_args,
    description="A YAML based pipeline which contains three steps",
    schedule=None,
    catchup=False,
    params=ParamsDict(
        {
            "configuration_file_key": Param(type="string", default=""),
        }
    ),
)


def first_step(configuration_file_key: str) -> None:
    # Hardcoded for testing, define them in real DAG
    bucket_name = "poc-dataingest-data-source-swissgeo"

    converter_file = download_from_s3(configuration_file_key, bucket_name)
    converter_definition = parse_yaml(converter_file)

    nodes = generate_node_tree(converter_definition, "first_step")

    if len(nodes) == 0:
        raise Exception("No nodes generated")
    apply_nodes(nodes)

    logger.info("first_step completed successfully")


def second_step(configuration_file_key: str) -> None:
    # Hardcoded for testing, define them in real DAG
    bucket_name = "poc-dataingest-data-source-swissgeo"

    converter_file = download_from_s3(configuration_file_key, bucket_name)
    converter_definition = parse_yaml(converter_file)

    nodes = generate_node_tree(converter_definition, "second_step")

    if len(nodes) == 0:
        raise Exception("No nodes generated")
    apply_nodes(nodes)

    logger.info("second_step completed successfully")


def third_step(configuration_file_key: str) -> None:
    # Hardcoded for testing, define them in real DAG
    bucket_name = "poc-dataingest-data-source-swissgeo"

    converter_file = download_from_s3(configuration_file_key, bucket_name)
    converter_definition = parse_yaml(converter_file)

    nodes = generate_node_tree(converter_definition, "third_step")

    if len(nodes) == 0:
        raise Exception("No nodes generated")
    apply_nodes(nodes)

    logger.info("third_step completed successfully")


# Define tasks
first_step_task = PythonOperator(
    task_id="first_step_task",
    python_callable=first_step,
    dag=dag,
    op_kwargs={
        "configuration_file_key": "{{ params.configuration_file_key }}",
    },
)

second_step_task = PythonOperator(
    task_id="second_step_task",
    python_callable=second_step,
    dag=dag,
    op_kwargs={
        "configuration_file_key": "{{ params.configuration_file_key }}",
    },
)

third_step_task = PythonOperator(
    task_id="third_step_task",
    python_callable=third_step,
    dag=dag,
    op_kwargs={
        "configuration_file_key": "{{ params.configuration_file_key }}",
    },
)

# Set dependencies between steps
first_step_task >> second_step_task >> third_step_task
