.PHONY: up down restart build shell lint test format

up:
	docker-compose up

down:
	docker-compose down

build-up:
	docker-compose up --build

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

build-up-auth-service:
	docker-compose up --build auth-service

build-up-api-gateway:
	docker-compose up --build api-gateway

build-up-chatbot-service:
	docker-compose up --build chatbot-service

build-up-conversation-service:
	docker-compose up --build conversation-service

restart-auth-service:
	docker-compose down auth-service
	docker-compose up --build auth-service

restart-api-gateway:
	docker-compose down api-gateway
	docker-compose up --build api-gateway

restart-chatbot-service:	
	docker-compose down chatbot-service
	docker-compose up --build chatbot-service

restart-conversation-service:
	docker-compose down conversation-service
	docker-compose up --build conversation-service

restart-all:
	docker-compose down
	docker-compose up --build