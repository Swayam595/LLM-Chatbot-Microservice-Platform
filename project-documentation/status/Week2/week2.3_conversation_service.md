# ✅ Week 2: `conversation-service` Implementation Summary

This document outlines the key design, development, and decisions made for the `conversation-service` as part of Week 2 implementation of the LLM chatbot platform.

---

## 📌 Objective

The `conversation-service` is responsible for:
- Storing and retrieving user chat history
- Caching recent messages for fast access
- Supporting semantic search using a Vector DB (ChromaDB)

---

## ✅ Features Implemented

### 1. 🎯 Core Functionality
- **POST `/conversations/message`**  
  → Create a new conversation entry

- **GET `/conversations/user/{user_id}`**  
  → Retrieve all conversations for a user (from Redis or DB)

---

### 2. 🗃️ PostgreSQL Integration
- SQLAlchemy async setup with `asyncpg`
- Alembic-compatible models (`Conversation`)
- Auto-creation of `convo_db` via Docker and init script

---

### 3. 🚀 Redis Caching
- Used for fast retrieval of recent conversation history
- TTL of 10 minutes added per user cache key
- JSON serialization handled with custom encoder

---

### 4. 🧠 Vector DB Integration
- ChromaDB run as a service in Docker
- Endpoints for:
  - `add_embedding()`: Add embeddings + metadata
  - `search_similar()`: Search semantically similar entries

---

## 🧪 Health Checks

- `/health` endpoint for general service check
- `/health/redis` added for Redis availability

---

## 🔐 Access Control

- This service is **not public**.
- Requests flow through the API Gateway, which:
  - Validates JWT
  - Forwards user data to the conversation-service
  - Handles RBAC (if needed)

---

## 🚫 Skipped (for now)
- Unit tests (to be added in Week 3)
- Kafka or background worker setup
- Rate-limiting, pagination on history API

---

## 🛠️ Dev Notes

- Ports used: `8003` for service, `8000` for ChromaDB container
- Environment variables:
  - `DATABASE_URL`
  - `REDIS_URL`
  - `CHROMA_DB_URL`

---

## 📁 Directory Highlights

```
conversation-service/
│
├── app/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── models/
│   ├── schemas/
│   └── dependencies/
│
├── Dockerfile
├── pyproject.toml
└── .env
```

---

## ✅ Status Summary

| Item                                       | Priority | Status     |
| ------------------------------------------|----------|------------|
| Core APIs                                  | High     | ✅ Done     |
| PostgreSQL + Redis                         | High     | ✅ Done     |
| Vector DB (ChromaDB)                       | Medium   | ✅ Done     |
| Health check                               | Low      | ✅ Done     |
| Unit tests                                 | Medium   | ❌ Skipped  |
| Access control                             | High     | ✅ (via Gateway) |
| OpenAPI tags / docs                        | Low      | ✅ Pending  |

---

**Next Step:** Begin work on `chatbot-service`
