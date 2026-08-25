# Local Airflow Dag container

This example extends the Airflow image used by this repository and copies the
Dag files into `${AIRFLOW_HOME}/dags`, following the Airflow Helm chart's
[bake Dags in a Docker image](https://airflow.apache.org/docs/helm-chart/stable/manage-dag-files.html#bake-dags-in-docker-image)
approach.

## Python dependencies

Runtime and development dependencies are managed with
[uv](https://docs.astral.sh/uv/). The Docker build installs the runtime set from
`uv.lock`; Ruff is a development dependency used for local Dag formatting.
Airflow itself is supplied by the base container image and is kept pinned
during dependency installation.

```bash
make setup
make lint
```

Add a runtime dependency and refresh the lockfile with:

```bash
uv add <package>
```

Commit both `pyproject.toml` and `uv.lock` after changing dependencies.

## Example Dags

- `local_airflow_example` is a minimal scheduled TaskFlow Dag.
- `restricted_service_account_example` is manually triggered and overrides its
  KubernetesExecutor worker pod to use the
  `airflow-worker-kubernetes-restricted` service account in the `airflow`
  namespace.

## Build and push

```bash
make dockerlogin
make dockerpush
```

`dockerpush` runs `dockerbuild` first. Use `make git-info` to print the exact
image tag before building or deploying it.

The image is tagged as:

```text
025064823138.dkr.ecr.eu-central-1.amazonaws.com/poc-datapipeline-repositories/airflow-dags:local-<user>-<git-hash>
```

Use the repository and generated tag in the Airflow Helm values:

```yaml
images:
  airflow:
    repository: 025064823138.dkr.ecr.eu-central-1.amazonaws.com/poc-datapipeline-repositories/airflow-dags
    tag: local-<user>-<git-hash>
```
