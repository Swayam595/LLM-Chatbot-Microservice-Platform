.PHONY: up down restart build shell lint test format

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

restart:
	make down
	make build
	make up

start-all:
	make build
	make up

restart-all:
	make down
	make start-all

shell:
	poetry shell

lint:
	ruff check .

format:
	ruff format .

test:
	pytest -v

build-up-auth-service:
	docker-compose build auth-service
	docker-compose up auth-service

build-up-api-gateway:
	docker-compose build api-gateway
	docker-compose up api-gateway

build-up-chatbot-service:
	docker-compose build chatbot-service
	docker-compose up chatbot-service

build-up-conversation-service:
	make build-up-chromadb
	make build-up-postgres
	make build-up-redis
	docker-compose build conversation-service
	docker-compose up conversation-service

build-up-conversation-service:
	docker-compose build conversation-service
	docker-compose up conversation-service

restart-auth-service:
	docker-compose down auth-service
	make build-up-auth-service

restart-api-gateway:
	docker-compose down api-gateway
	make build-up-api-gateway

restart-chatbot-service:	
	docker-compose down chatbot-service
	make build-up-chatbot-service

restart-conversation-service:
	docker-compose down conversation-service
	make build-up-conversation-service

build-up-postgres:
	docker-compose build postgres
	docker-compose up postgres

build-up-chromadb:
	docker-compose build chromadb
	docker-compose up chromadb

restart-postgres:
	docker-compose down postgres
	make build-up-postgres

open-auth-db:
	docker exec -it postgres psql -U user -d auth_db

open-convo-db:
	docker exec -it postgres psql -U user -d convo_db

open-redis-cli:
	docker exec -it redis redis-cli

remove-all:
	docker-compose down --volumes --remove-orphans

remove-postgres-data:
	docker volume rm llm-chatbot-services_postgres_data