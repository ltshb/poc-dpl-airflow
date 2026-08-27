# Local Airflow DAG sidecar

This example packages DAG files in a small image and copies them once into a
shared `emptyDir` volume using an init container. The init container exits after
the copy completes, allowing the Airflow containers to start.

The image owns the `local-airflow-dag-sidecar` subdirectory in the shared DAG
volume without removing DAGs deployed by other mechanisms. Updating the DAGs
requires publishing a new image tag and rolling out the Airflow workloads.

## Python development

Development dependencies are managed with [uv](https://docs.astral.sh/uv/).
Airflow is supplied by the deployed Airflow containers and is therefore not a
dependency of this DAG-only image.

```bash
make setup
make lint
```

After changing dependencies, commit both `pyproject.toml` and `uv.lock`.

## Build and push

```bash
make dockerlogin
make dockerpush
```

The image is tagged as:

```text
025064823138.dkr.ecr.eu-central-1.amazonaws.com/poc-datapipeline/airflow-dags-only:sidecar-local-<user>-<git-hash>
```

After changing the image tag, update every DAG deployer image reference in
`kubernetes/base/manifets/values.yaml`, regenerate the rendered manifest as
described in `kubernetes/README.md`, and deploy it.
