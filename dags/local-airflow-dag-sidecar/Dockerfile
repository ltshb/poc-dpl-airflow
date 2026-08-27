FROM busybox:1.37.0

COPY --chown=50000:0 dags/ /opt/airflow/dag-source/
COPY --chown=50000:0 --chmod=0555 deploy-dags.sh /usr/local/bin/deploy-dags

USER 50000:0

ENTRYPOINT ["/usr/local/bin/deploy-dags"]
