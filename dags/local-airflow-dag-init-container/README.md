# Local Airflow DAG init container

This example packages DAG files in a small image and copies them once into a
shared `emptyDir` volume using an init container. The init container exits after
the copy completes, allowing the Airflow containers to start.

The image owns the `local-airflow-dag-init-container` subdirectory in the shared DAG
volume without removing DAGs deployed by other mechanisms. Updating the DAGs
requires publishing a new image tag and rolling out the Airflow workloads.

## Python development

Runtime and development dependencies are managed with
[uv](https://docs.astral.sh/uv/). The image build installs locked runtime
dependencies into a `python` directory that the init container copies alongside
the DAG. The Airflow components that consume this volume include that directory
in `PYTHONPATH`, allowing DAG files to use normal top-level imports. Airflow
itself is supplied by the deployed Airflow containers and is therefore not a
dependency of this DAG-only image.

```bash
make setup
make lint
```

Configure your IDE to use the `.venv` created by `make setup`; imports from UV
dependencies will then resolve during editing as well.

Add another runtime dependency with:

```bash
uv add <package>
```

After changing dependencies, commit both `pyproject.toml` and `uv.lock`.

## Build and push

```bash
make dockerlogin
make dockerpush
```

The image is tagged as:

```text
025064823138.dkr.ecr.eu-central-1.amazonaws.com/poc-datapipeline/airflow-dags-only:init-local-<user>-<git-hash>
```

After changing the image tag, update `dagInitContainerImage.tag` in
`kubernetes/base/manifets/values.yaml`, regenerate the rendered manifest as
described in `kubernetes/README.md`, and deploy it.
