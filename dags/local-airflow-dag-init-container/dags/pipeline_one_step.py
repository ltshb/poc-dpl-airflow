import logging

from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG
from airflow.sdk.definitions.param import Param, ParamsDict
from pipeline_tooling.from_nodes import apply_nodes, generate_node_tree
from pipeline_tooling.importer import download_from_s3
from pipeline_tooling.reader import parse_yaml

logger = logging.getLogger("pipeline_one_step")

# Define default arguments for the DAG
default_args = {"owner": "airflow", "depends_on_past": False, "retries": 0}

# Create the DAG
dag = DAG(
    "one_step_pipeline",
    default_args=default_args,
    description="A YAML based pipeline which contains one step",
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


first_step_task = PythonOperator(
    task_id="first_step_task",
    python_callable=first_step,
    dag=dag,
    op_kwargs={
        "configuration_file_key": "{{ params.configuration_file_key }}",
    },
)
