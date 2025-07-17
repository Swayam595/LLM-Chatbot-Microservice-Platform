.PHONY: up down restart build shell lint test format

up:
	docker-compose up --build

down:
	docker-compose down

restart:
	docker-compose down && docker-compose up --build

build:
	docker-compose build

shell:
	poetry shell

lint:
	ruff check .

format:
	ruff format .

test:
	pytest -v
