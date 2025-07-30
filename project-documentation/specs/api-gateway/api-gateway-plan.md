# ✅ API Gateway - Plan & Implementation Checklist (Week 3)

This checklist outlines the implementation plan and current progress for building the `api-gateway` microservice.

---

## 1. 🧱 Project Skeleton - ✅ 

| Task                                | Status | Notes                        |
| ----------------------------------- | ------ | ---------------------------- |
| Initialize FastAPI app in `main.py` | ✅      | With health check            |
| Create directory structure          | ✅      | `routes/`, `services/`, etc. |

**Structure:**

```
api_gateway/
├── app/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── middlewares/
│   ├── utils/
│   ├── dependencies/
│   └── config.py
```

---

## 2. 🚪 Routing & Proxying

| Task                                               | Status | Notes                                    |
| -------------------------------------------------- | ------ | ---------------------------------------- |
| Route `/chatbot/chat` to chatbot-service           | [ ]      | Uses internal DNS `chatbot-service:8002` |
| Route `/auth/verify` to auth-service               | [ ]      | Verifies token via `/verify-token`       |
| Route `/conversations/...` to conversation-service | [ ]      | Needed for context and storing messages  |

---

## 3. 🔐 Authentication Middleware

| Task                             | Status | Notes                                  |
| -------------------------------- | ------ | -------------------------------------- |
| Middleware to intercept requests | [ ]      | Skips `/auth` routes                   |
| Forward token to auth-service    | [ ]      | Handles 401 and service unavailability |

---

## 4. 💨 Rate Limiting

| Task                          | Status | Notes                                               |
| ----------------------------- | ------ | --------------------------------------------------- |
| Basic in-memory rate limiting | [ ]      | Per-IP based window (temporary)                     |
| Redis-backed limiter          | \2b1c  | Planned for later (production-ready implementation) |

---

## 5. 💾 Request/Response Logging

| Task                     | Status | Notes                            |
| ------------------------ | ------ | -------------------------------- |
| Log method, path, status | [ ]      | Middleware added for logging     |
| Add request ID tracing   | \2b1c  | Optional, for cross-service logs |

---

## 6. 🧠 Utilities and Forwarding

| Task                                | Status | Notes                                |
| ----------------------------------- | ------ | ------------------------------------ |
| Abstract `httpx` forwarder function | [ ]      | Used for GET, POST to other services |
| Error handling around timeouts      | [ ]      | Graceful fallback w/ `503` or retry  |

---

## 7. 🦪 Error Handling

| Task                                    | Status | Notes                                        |
| --------------------------------------- | ------ | -------------------------------------------- |
| ServiceError wrapper                    | [ ]      | Uniform error reporting                      |
| Handle 4xx/5xx from downstream services | [ ]      | Translates httpx errors to FastAPI responses |

---

## 8. 📜 Swagger & API Tags

| Task                   | Status | Notes                       |
| ---------------------- | ------ | --------------------------- |
| Add OpenAPI tags       | [ ]      | Group routes by service     |
| Customize API metadata | [ ]      | Title, description, version |

---

## 9. 🚣 Docker & Compose Integration

| Task                        | Status | Notes                                  |
| --------------------------- | ------ | -------------------------------------- |
| Add Dockerfile              | ✅      | Based on FastAPI + Poetry              |
| Add to `docker-compose.yml` | ✅      | Depends on auth, chatbot, conversation |
| Expose on `localhost:8000`  | ✅      | Main entry point for frontend/clients  |

---

## 🔮 Future Enhancements

* \2b1c Add JWT verification locally for fallback (optional)
* \2b1c Add request ID in headers for tracing
* \2b1c Add circuit breaker or retry with `tenacity`
* \2b1c Implement service registry / discovery (later)

---

**Progress should be checked off as development continues.**
