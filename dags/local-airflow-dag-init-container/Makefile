SHELL = /bin/bash

.DEFAULT_GOAL := help

SERVICE_NAME := airflow-dags-only

GIT_HASH_SHORT := $(shell git rev-parse --short HEAD)
DOCKER_REGISTRY := 025064823138.dkr.ecr.eu-central-1.amazonaws.com
ECR_REPOSITORY := poc-datapipeline/$(SERVICE_NAME)
DOCKER_IMG_LOCAL_TAG := $(DOCKER_REGISTRY)/$(ECR_REPOSITORY):init-local-$(USER)-$(GIT_HASH_SHORT)
AWS_REGION := eu-central-1
AWS_PROFILE := swisstopo-swissgeo-poc-datapipeline

UV_RUN := uv run
RUFF := $(UV_RUN) ruff

.PHONY: ci
ci: ## Install exactly the dependencies recorded in uv.lock
	uv sync --frozen

.PHONY: setup
setup: ## Create or update the local uv environment
	uv sync

.PHONY: format
format: ## Format and sort imports in the DAG source
	$(RUFF) format dags
	$(RUFF) check --select I --fix dags

.PHONY: lint
lint: ## Check the DAG source with Ruff
	$(RUFF) check dags
	$(RUFF) format --check dags

.PHONY: dockerlogin
dockerlogin: ## Log in to the AWS ECR registry
	aws --profile $(AWS_PROFILE) ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(DOCKER_REGISTRY)

.PHONY: dockerbuild
dockerbuild: ## Build the DAG init-container image
	docker build --tag $(DOCKER_IMG_LOCAL_TAG) .

.PHONY: dockerpush
dockerpush: dockerbuild ## Build and push the DAG init-container image to ECR
	docker push $(DOCKER_IMG_LOCAL_TAG)

.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"} \
	/^[a-zA-Z0-9_.-]+:.*##/ { printf "%-15s %s\n", $$1, $$2 }' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN { printf "\nUsage:\n  make \033[36m<target>\033[0m\n\n" } \
	{ printf "  \033[36m%-15s\033[0m %s\n", $$1, substr($$0, index($$0,$$2)) }'
