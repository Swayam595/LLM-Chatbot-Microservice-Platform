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

open-auth-db:
	docker exec -it postgres psql -U user -d auth_db

remove-postgres-data:
	docker volume rm llm-chatbot-services_postgres_data