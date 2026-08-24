FROM apache/airflow:3.2.2

ARG GIT_HASH="unknown"
ARG GIT_BRANCH="unknown"
ARG GIT_DIRTY=""
ARG VERSION="unknown"
ARG AUTHOR="unknown"

LABEL org.opencontainers.image.authors="${AUTHOR}" \
      org.opencontainers.image.revision="${GIT_HASH}" \
      org.opencontainers.image.version="${VERSION}" \
      ch.swisstopo.git.branch="${GIT_BRANCH}" \
      ch.swisstopo.git.dirty="${GIT_DIRTY}"

# The Airflow image already provides uv. Export the locked runtime dependencies
# and install them into Airflow's existing Python environment. Pinning Airflow in
# the same command prevents the resolver from changing the base image version.
COPY --chown=airflow:root pyproject.toml uv.lock /opt/airflow/dag-project/
WORKDIR /opt/airflow/dag-project
RUN uv export \
        --locked \
        --no-dev \
        --no-emit-project \
        --no-hashes \
        --format requirements-txt \
        --output-file /tmp/dag-requirements.txt \
    && uv pip install \
        --no-cache \
        "apache-airflow==${AIRFLOW_VERSION}" \
        --requirements /tmp/dag-requirements.txt \
    && rm /tmp/dag-requirements.txt

WORKDIR ${AIRFLOW_HOME}
COPY --chown=airflow:root ./dags/ ${AIRFLOW_HOME}/dags/
