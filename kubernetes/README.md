# Install Airflow on Kubernetes

```bash
helm repo add apache-airflow https://airflow.apache.org
```

```bash
helm template apache-airflow/airflow --values kubernetes/base/manifets/values.yaml --namespace airflow > kubernetes/base/manifets/rendered.yaml
```

## Helm values

Based on https://airflow.apache.org/docs/helm-chart/stable/index.html#installing-the-helm-chart-with-argo-cd-flux-rancher-or-terraform

## Database

The database is setup using AWS RDS. In order to connect to the database we had to first create
the databas `airflow-db`. For the DB see https://github.com/swissgeo/infra-terraform/pull/479

For manual DB create do

```bash
# misused the service-oa-features-rds-proxy for db access
kubectl port-forward -n service-oa-features deploy/service-oa-features-rds-proxy 5432:5432
psql -h localhost -p 5432 -U postgres
CREATE DATABASE "airflow-db";
```

## TODO

- [ ] Setup Secrets see https://airflow.apache.org/docs/helm-chart/stable/production-guide.html#api-secret-key
