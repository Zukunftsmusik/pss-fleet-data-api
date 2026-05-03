.PHONY: all
all: format check test

# setup
.PHONY: init-dev
init-dev:
	uv self update
	uv sync
	pre-commit install
	pre-commit run --all-files

.PHONY: update
update:
	uv sync --upgrade


# dev tools
.PHONY: lock
lock:
	uv export --no-hashes --no-header --no-annotate --no-dev --format requirements.txt > requirements.txt
	uv export --no-hashes --no-header --no-annotate --format requirements.txt > requirements-dev.txt


# formatting and linting
.PHONY: check
check:
	uv run --no-project ruff check ./src
	uv run --no-project vulture ./src

.PHONY: format
format:
	uv run --no-project ruff check --fix ./src ./tests
	uv run --no-project ruff format ./src ./tests


# testing
.PHONY: coverage
coverage:
	uv run --no-project pytest --cov=./src/api --cov-report=xml:cov.xml --cov-report=term

.PHONY: test
test:
	uv run --no-project pytest tests

# run
.PHONY: rundev
rundev:
	uv run fastapi dev src/api/main.py

.PHONY: docker
docker:
	-docker stop container-pss-fleet-data-api
	docker rm -f container-pss-fleet-data-api
	docker image rm -f image-pss-fleet-data-api:latest
	docker build -t image-pss-fleet-data-api .
	docker run -d --name container-pss-fleet-data-api -p 8000:80 --env-file ./.docker-env image-pss-fleet-data-api:latest

.PHONY: run
run:
	uv run fastapi run src/api/main.py
