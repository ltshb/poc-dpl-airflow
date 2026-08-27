#!/bin/sh

set -eu

readonly source_dir="${DAG_SOURCE_DIR:-/opt/airflow/dag-source}"
readonly target_root="${DAG_TARGET_DIR:-/opt/airflow/dags}"
readonly bundle_name="${DAG_BUNDLE_NAME:-local-airflow-dag-init-container}"
readonly destination="${target_root}/${bundle_name}"
readonly staging="${target_root}/.${bundle_name}.staging"

rm -rf "${staging}"
mkdir -p "${staging}"
cp -R "${source_dir}/." "${staging}/"
rm -rf "${destination}"
mv "${staging}" "${destination}"
