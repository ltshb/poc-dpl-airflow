# Install Airflow on Kubernetes

```bash
helm repo add apache-airflow https://airflow.apache.org
```

```bash
helm template apache-airflow/airflow --values kubernetes/base/manifets/values.yaml --namespace airflow > kubernetes/base/manifets/rendered.yaml
```

## Helm values

Based on https://airflow.apache.org/docs/helm-chart/stable/index.html#installing-the-helm-chart-with-argo-cd-flux-rancher-or-terraform

## TODO

- [ ] Setup Secrets see https://airflow.apache.org/docs/helm-chart/stable/production-guide.html#api-secret-key
