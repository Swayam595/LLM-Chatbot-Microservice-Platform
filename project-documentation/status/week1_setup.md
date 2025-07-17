# 🗓️ Week 1: Project Setup & Architecture

This document outlines the tasks completed in **Week 1** for the LLM-powered chatbot microservices platform.

---

## ✅ Completed Tasks

### 1. Define Core Features and Microservices

- **auth-service**: User registration, login, JWT authentication
- **chatbot-service**: Handles user prompts, response generation (LLM integration)
- **conversation-service**: Stores and retrieves chat history
- **api-gateway**: Single entrypoint for frontend/client, routes to internal services

---

### 2. Design High-Level Architecture

- Defined the microservices and their responsibilities
- Created a **textual architecture diagram** listing components like:
  - `Frontend` → `API Gateway`
  - `API Gateway` → `Auth`, `Chatbot`, `Conversation`
- Added shared utilities under `shared/` folder (e.g., logging, database, JWT utils)

---

### 3. Set Up Monorepo with Poetry

- Root folder: `llm-chatbot-services/`
- Tool: [`Poetry`](https://python-poetry.org/)
- Each microservice is a self-contained Poetry-managed module

Example layout:

```
llm-chatbot-services/
├── docker-compose.yml
├── Makefile
├── services/
│   ├── auth_service/
│   │   ├── app/
│   │   ├── pyproject.toml
│   │   └── Dockerfile
│   ├── chatbot_service/
│   ├── conversation_service/
│   └── api_gateway/
```

---

### 4. Scaffolded Each Microservice

Each folder contains:

- `app/main.py`: FastAPI app with basic `/` and `/health` routes
- `pyproject.toml`: Poetry setup
- `Dockerfile`: FastAPI running on Uvicorn in a container

✅ Completed for:  
- `auth_service`
- `api_gateway`
- `chatbot_service`
- `conversation_service`

---

### 5. Created Docker + Makefile Setup

- **`docker-compose.yml`** at root to orchestrate all services
- **`Makefile`** to simplify dev commands:
  - `make up` → builds and starts all containers
  - `make down` → stops all containers
  - `make restart` → rebuilds and restarts

---

### 6. Auth Service Running in Docker

- `auth_service` builds successfully
- Runs inside Docker container on port `8001`
- Health check at `http://localhost:8001/health` responds with `{ "status": "ok" }`

---

## 📂 Related Files Created

- `features_and_architecture.md`
- `high_level_architecture.md`
- `project_timeline.md`
- `docker-compose.yml`
- `Makefile`
- `services/auth_service/app/main.py`
- `services/auth_service/Dockerfile`
- `services/auth_service/pyproject.toml`
- `services/api_gateway/app/main.py`
- `services/api_gateway/Dockerfile`
- `services/api_gateway/pyproject.toml`
- `services/chatbot_service/app/main.py`
- `services/chatbot_service/Dockerfile`
- `services/chatbot_service/pyproject.toml`
- `services/conversation_service/app/main.py`
- `services/conversation_service/Dockerfile`
- `services/conversation_service/pyproject.toml`


---

## 🧠 What’s Next

Move into **Week 2: Authentication Logic**

- Implement `/register` endpoint in `auth_service`
- Add input validation and password hashing
- Optional: connect to SQLite or PostgreSQL DB

