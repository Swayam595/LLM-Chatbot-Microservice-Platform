# ✅ Chatbot Service - Week 2 Plan & Implementation Checklist

This markdown outlines the step-by-step implementation plan for the `chatbot-service` and serves as a checklist for tracking progress.

---

## 1. 🧱 Project Skeleton
- ✅ Set up `main.py` with FastAPI app and health check
- ✅ Create and organize directories:
  - ✅ `routes/`
  - ✅ `services/`
  - ✅ `schemas/`
  - ✅ `llm/`
  - ✅ `dependencies/`
  - ✅ `utils/`

---

## 2. 💬 Input Handling Route
- ✅ Create `POST /chat` endpoint
- ✅ Accept `user_id` and `message`
- ✅ Validate input and pass to service layer

---

## 3. 🧠 Prompt Construction
- ✅ Hybrid Prompt Construction in the chatbot service using both:
  - 🕓 Recent chat history (from conversation-service)
  - 🔍 Semantically similar past messages (via ChromaDB)
- ✅ Construct context-aware prompt using user history

---

## 4. 🤖 LLM Integration
- ✅ Integrate Gemini API
- ✅ Implement Strategy pattern for LLM abstraction

---

## 5. 📤 Response Handling
- ✅ Return generated response to client
- ✅ Persist response and message via `conversation-service`

---

## 6. 🧩 Tool/Agent Support (Optional)
- [ ] Add stub for external tool/agent API integration

---

## 7. 🛡️ Error Handling & Logging
- [ ] Log each request and response (basic info)
- [ ] Gracefully handle downstream service failures
- [ ] Add retry/backoff logic (optional enhancement)

---

**Progress should be checked off as development continues.**