DOCKER_COMPOSE = docker compose

# Include file with environment variables if it exists
-include Makefile.env

# Default target when running `make`
all: docker-up

PROXY_RUN = $(DOCKER_COMPOSE) run --rm proxy

# Container management
# --------------------

.PHONY: config
config: .env config.yaml

# Create .env file to set the UID/GID for the docker containers to run as to the current user
.env:
	echo "DOCKER_LOCAL_USER=$(shell id -u):$(shell id -g)" >> .env

# Create config file from config_dist_dev.yaml if it does not exist yet
config.yaml:
	cp config_dist_dev.yaml config.yaml

.PHONY: docker-up
docker-up: docker-build
	$(DOCKER_COMPOSE) up

.PHONY: docker-down
docker-down: config
	$(DOCKER_COMPOSE) down --remove-orphans

.PHONY: docker-purge
docker-purge: config
	$(DOCKER_COMPOSE) down --remove-orphans --volumes

.PHONY: docker-build
docker-build: config
	$(DOCKER_COMPOSE) build proxy


# Start a shell (bash) in the quart docker container
.PHONY: docker-shell
docker-shell:
	$(PROXY_RUN) bash


.PHONY: lint-fix
lint-fix:
	ruff check --fix ./app
	black ./app
	# mypy has no fix mode, we run it anyway to report (unfixable) errors
	mypy ./app

.PHONY: lint-check
lint-check:
	ruff check ./app
	black -S --check --diff app
	mypy ./app
