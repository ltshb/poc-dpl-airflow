SHELL = /bin/bash

.DEFAULT_GOAL := help

SERVICE_NAME := airflow-dags

# Docker metadata
GIT_HASH := $(shell git rev-parse HEAD)
GIT_HASH_SHORT := $(shell git rev-parse --short HEAD)
GIT_BRANCH := $(shell git symbolic-ref HEAD --short 2>/dev/null)
GIT_DIRTY := $(shell git status --porcelain)
GIT_TAG := $(shell git describe --tags 2>/dev/null || echo "no version info")
AUTHOR := $(USER)

# Commands
UV_RUN := uv run
RUFF := $(UV_RUN) ruff

# Docker variables
DOCKER_REGISTRY := 025064823138.dkr.ecr.eu-central-1.amazonaws.com
ECR_REPOSITORY := poc-datapipeline/$(SERVICE_NAME)
DOCKER_IMG_LOCAL_TAG := $(DOCKER_REGISTRY)/$(ECR_REPOSITORY):local-$(USER)-$(GIT_HASH_SHORT)

# AWS variables
AWS_REGION := eu-central-1
AWS_PROFILE := swisstopo-swissgeo-poc-datapipeline

.PHONY: ci
ci: ## Install exactly the dependencies recorded in uv.lock
	uv sync --frozen

.PHONY: setup
setup: ## Create or update the local uv environment
	uv sync

.PHONY: format
format: ## Format and sort imports in the Dag source
	$(RUFF) format dags
	$(RUFF) check --select I --fix dags

.PHONY: lint
lint: ## Check the Dag source with Ruff
	$(RUFF) check dags
	$(RUFF) format --check dags

.PHONY: git-info
git-info: ## Print the current version and image information
	@echo "GIT_HASH=$(GIT_HASH)"
	@echo "GIT_HASH_SHORT=$(GIT_HASH_SHORT)"
	@echo "GIT_BRANCH=$(GIT_BRANCH)"
	@echo "GIT_DIRTY=$(GIT_DIRTY)"
	@echo "GIT_TAG=$(GIT_TAG)"
	@echo "AUTHOR=$(AUTHOR)"
	@echo "DOCKER_IMG_LOCAL_TAG=$(DOCKER_IMG_LOCAL_TAG)"

.PHONY: dockerlogin
dockerlogin: ## Log in to the AWS ECR registry
	aws --profile $(AWS_PROFILE) ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(DOCKER_REGISTRY)

.PHONY: dockerbuild
dockerbuild: ## Build the Airflow image containing the example Dag
	docker build \
		--build-arg GIT_HASH="$(GIT_HASH)" \
		--build-arg GIT_BRANCH="$(GIT_BRANCH)" \
		--build-arg GIT_DIRTY="$(GIT_DIRTY)" \
		--build-arg VERSION="$(GIT_TAG)" \
		--build-arg AUTHOR="$(AUTHOR)" \
		--tag $(DOCKER_IMG_LOCAL_TAG) .

.PHONY: dockerpush
dockerpush: dockerbuild ## Build and push the Airflow image to ECR
	set -o pipefail; \
	docker push $(DOCKER_IMG_LOCAL_TAG) 2>&1 | grep --color=always -E "tag invalid: .*|$$"

.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"} \
	/^[a-zA-Z0-9_.-]+:.*##/ { printf "%-15s %s\n", $$1, $$2 }' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN { printf "\nUsage:\n  make \033[36m<target>\033[0m\n\n" } \
	{ printf "  \033[36m%-15s\033[0m %s\n", $$1, substr($$0, index($$0,$$2)) }'
