# 🗓️ Week 2: Auth Service - Register & Login

This document captures the progress and remaining tasks for **Week 2** of the LLM Chatbot Microservice project.

---

## ✅ Completed Tasks

### 1. Implement `/register` endpoint in `auth_service`

* Created `UserCreate` schema with validation using Pydantic.
* Passwords hashed securely using **bcrypt** with `passlib`.
* Registered users stored in **PostgreSQL** using SQLAlchemy.
* Error handling for duplicate email registration.

### 2. Setup PostgreSQL

* Added `postgres` container in `docker-compose.yml`.
* Connection string injected using `DATABASE_URL` env var.
* `database.py` implemented using **SQLAlchemy AsyncSession**.
* Connection follows **SOLID** principles and clean structure.

### 3. Implement `/login` endpoint in `auth_service`

* Login schema validated with `UserLogin` Pydantic model.
* JWT generated using `python-jose` and `HS256` algorithm.
* Environment variables used for `SECRET_KEY`, `ALGORITHM`, and `EXPIRY`.
* Tokens returned as `{ access_token, token_type }`.

### 4. Configuration Handling

* Central `config.py` reads from `.env` via `python-dotenv`.
* Injected config into services instead of hardcoding values.

### 5. Dockerized Auth Service

* Updated `Dockerfile` to use Poetry and copy `.env`.
* Added `PYTHONPATH=/app` for cross-module imports.
* `auth_service` runs on `localhost:8001`.

### 6. Imports and Path Fixes

* Adjusted VS Code settings for `python.analysis.extraPaths`.
* Ensured relative imports work with `PYTHONPATH` set in compose.

### 7. ✅ Logging Setup

* Shared `Logger` class added under `shared/`
* Reads `LOG_LEVEL` from environment variables
* Injected into all service constructors for consistent logging
* Used across `/register` and `/login` flows

---

## ⚡ Remaining Tasks for Week 2

* [ ] Begin writing unit tests for `/register` and `/login`
* [ ] Write documentation for `auth_service` endpoints
* [ ] Implement JWT authentication middleware
* [ ] Add current user dependency using `Depends`

---

## 📁 Related Files Added

* `services/auth_service/app/main.py`
* `services/auth_service/app/schemas/user_create.py`, `user_login.py`
* `services/auth_service/app/services/user_service.py`
* `services/auth_service/app/repositories/user_repository.py`
* `services/auth_service/app/services/database.py`
* `services/auth_service/config.py`
* `shared/logger.py`
* `.env`, `Dockerfile`, `docker-compose.yml`, `Makefile`

---

Would you like to:

* Continue with JWT auth middleware?
* Move to `chatbot_service` scaffolding next?
