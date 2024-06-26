.PHONY: all
all: format check test

.PHONY: init
init:
	rye init

.PHONY: sync
sync:
	rye sync

.PHONY: test
test:
	rye run pytest

.PHONY: format
format:
	rye run autoflake .
	rye run isort .
	rye run black .

.PHONY: check
check:
	rye run flake8 .

.PHONY: run
run:
	fastapi dev src/main.py

.PHONY: docker
docker:
	-docker stop container-pss-fleet-data-api
	docker rm -f container-pss-fleet-data-api
	docker image rm -f image-pss-fleet-data-api:latest
	docker build -t image-pss-fleet-data-api .
	docker run -d --name container-pss-fleet-data-api -p 80:80 image-pss-fleet-data-api:latest