import logging

# import pyarrow.compute as pc
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG
from airflow.sdk.definitions.param import Param, ParamsDict
from pipeline_tooling.from_nodes import apply_nodes, generate_node_tree
from pipeline_tooling.importer import download_from_s3
from pipeline_tooling.reader import parse_yaml

logger = logging.getLogger("mch_forecast_values")

# Define default arguments for the DAG
default_args = {"owner": "airflow", "depends_on_past": False, "retries": 0}

# Create the DAG
dag = DAG(
    "pipeline_mch_forecast_values",
    default_args=default_args,
    description="A process to download and sanitize MCH forecast values data from S3",
    schedule=None,
    catchup=False,
    params=ParamsDict(
        {
            "csv_file_key": Param(type="string", default="vnut12.lssw.202608240800.tre200px.csv"),
            "configuration_file_key": Param(
                type="string", default="mch_forecast_value_tre200px.yaml"
            ),
        }
    ),
)


def download_and_parse_csv(csv_file_key: str, configuration_file_key: str) -> None:
    """
    Task that downloads a CSV from S3 and parses it into a PyArrow Table.
    """
    # Hardcoded for testing, define them in real DAG
    bucket_name = "poc-dataingest-data-source-swissgeo"

    # Download the CSV file from S3
    try:
        converter_file = download_from_s3(configuration_file_key, bucket_name)
        converter_definition = parse_yaml(converter_file)

        nodes = generate_node_tree(
            converter_definition, "download", params={"csv_file_key": csv_file_key}
        )
        if len(nodes) == 0:
            raise Exception("No nodes generated")
        apply_nodes(nodes)

    except Exception:
        logger.exception("Error in download_and_parse_csv task")
        raise


def sanitize_data(configuration_file_key: str) -> None:
    """
    Task that validates and converts the point data

    Converts the date column into a s3tables native date
    """

    # Hardcoded for testing, define them in real DAG
    bucket_name = "poc-dataingest-data-source-swissgeo"

    try:
        converter_file = download_from_s3(configuration_file_key, bucket_name)
        converter_definition = parse_yaml(converter_file)

        nodes = generate_node_tree(converter_definition, "sanitize")
        if len(nodes) == 0:
            raise Exception("No nodes generated")
        apply_nodes(nodes)

    except Exception as e:
        logger.exception("Error in sanitize_data task", exc_info=e)
        raise


def combine_and_export_data(configuration_file_key: str) -> None:
    bucket_name = "poc-dataingest-data-source-swissgeo"

    converter_file = download_from_s3(configuration_file_key, bucket_name)
    converter_definition = parse_yaml(converter_file)

    nodes = generate_node_tree(converter_definition, "load")
    if len(nodes) == 0:
        raise Exception("No nodes generated")
    apply_nodes(nodes)


download_and_parse_task = PythonOperator(
    task_id="download_and_parse_task",
    python_callable=download_and_parse_csv,
    dag=dag,
    op_kwargs={
        "csv_file_key": "{{ params.csv_file_key }}",
        "configuration_file_key": "{{ params.configuration_file_key }}",
    },
)

sanitize_task = PythonOperator(
    task_id="sanitize_task",
    python_callable=sanitize_data,
    dag=dag,
    op_kwargs={"configuration_file_key": "{{ params.configuration_file_key }}"},
)

combine_and_export_data_task = PythonOperator(
    task_id="combine_and_export_data_task",
    python_callable=combine_and_export_data,
    dag=dag,
    op_kwargs={"configuration_file_key": "{{ params.configuration_file_key }}"},
)

# ruff: ignore=unused-expression
download_and_parse_task >> sanitize_task >> combine_and_export_data_task
