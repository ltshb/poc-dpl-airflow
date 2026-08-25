import logging

from airflow.sdk import dag, task
from dateutil.parser import isoparse
from kubernetes.client import models as k8s

RESTRICTED_SERVICE_ACCOUNT = "airflow-worker-kubernetes-restricted"

RESTRICTED_WORKER_CONFIG = {
    "pod_override": k8s.V1Pod(
        metadata=k8s.V1ObjectMeta(
            labels={"example": "restricted-service-account"},
        ),
        spec=k8s.V1PodSpec(
            containers=[k8s.V1Container(name="base")],
            service_account_name=RESTRICTED_SERVICE_ACCOUNT,
        ),
    ),
}


@dag(
    dag_id="restricted_service_account_example",
    description="Run a KubernetesExecutor worker with the restricted service account.",
    schedule=None,
    start_date=isoparse("2026-01-01T00:00:00Z"),
    catchup=False,
    tags=["example", "kubernetes", "restricted"],
)
def restricted_service_account_example():
    @task(executor_config=RESTRICTED_WORKER_CONFIG)
    def report_service_account():
        logging.info(
            "This worker pod uses Kubernetes service account %s",
            RESTRICTED_SERVICE_ACCOUNT,
        )

    report_service_account()


restricted_service_account_example()
