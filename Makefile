DOCKER_COMPOSE = docker compose

# Include file with environment variables if it exists
-include Makefile.env

# Default target when running `make`
all: docker-up

PROXY_RUN = $(DOCKER_COMPOSE) run --rm proxy

# Container management
# --------------------

# Create .env file to set the UID/GID for the docker containers to run as to the current user
.env:
	echo "DOCKER_LOCAL_USER=$(shell id -u):$(shell id -g)" >> .env

.PHONY: docker-up
docker-up: docker-build
	$(DOCKER_COMPOSE) up

.PHONY: docker-down
docker-down: .env
	$(DOCKER_COMPOSE) down --remove-orphans

.PHONY: docker-purge
docker-purge: .env
	$(DOCKER_COMPOSE) down --remove-orphans --volumes

.PHONY: docker-build
docker-build: .env
	$(DOCKER_COMPOSE) build proxy


# Start a shell (bash) in the quart docker container
.PHONY: docker-shell
docker-shell:
	$(PROXY_RUN) bash


.PHONY: lint-fix
lint-fix:
	$(PROXY_RUN) ruff --fix ./app
	$(PROXY_RUN) black ./app

.PHONY: lint-check
lint-check:
	$(PROXY_RUN) ruff ./app
	$(PROXY_RUN) black -S --check --diff app
