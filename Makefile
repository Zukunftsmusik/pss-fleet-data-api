.PHONY: all
all: format check test

.PHONY: init
init:
	poetry install

.PHONY: test
test:
	poetry run pytest

.PHONY: format
format:
	@poetry run autoflake .
	@poetry run isort .
	@poetry run black .

.PHONY: check
check:
	@poetry run flake8 .

.PHONY: build
build:
	poetry build

.PHONY: docker
docker:
	-docker stop container-pss-fleet-data-api
	docker rm -f container-pss-fleet-data-api
	docker image rm -f image-pss-fleet-data-api:latest
	docker build -t image-pss-fleet-data-api .
	docker run -d --name container-pss-fleet-data-api -p 80:80 image-pss-fleet-data-api:latest