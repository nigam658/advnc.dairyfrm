# DairyOS AI — Dairy Farm Management Backend API

Backend system for managing dairy farm operations using FastAPI, MySQL, and Gemini AI.

Built with AI-powered backend workflows capable of processing natural language dairy queries through tool-calling architecture.

---

# Features

## Backend Features

* JWT authentication and refresh tokens
* Role-based authorization (RBAC)
* Cow management APIs
* Milk record management
* Pagination and sorting
* Query parameter filtering
* SQLAlchemy ORM integration
* Alembic migrations
* Validation and exception handling
* Modular service-layer architecture

---

# AI Features

* Gemini AI integration
* Natural language dairy queries
* AI tool-calling workflows
* Dynamic function routing
* AI-generated human-readable responses
* Real-time dairy analytics
* Intent-based backend execution

### Example AI Queries

```txt
today total milk
highest milk producing cow
monthly milk report
which cow gave highest milk this month
```

---

# Tech Stack

## Backend

* FastAPI
* Python
* SQLAlchemy
* Alembic

## Database

* MySQL

## AI Engineering

* Gemini AI
* Tool Calling
* Function Routing

## Security

* JWT Authentication
* RBAC Authorization

---

# Example APIs

```http
POST /login
POST /refresh-token

GET /cow?cow_tag=001
GET /cow/milkrecord?cow_tag=001&page=1&limit=5

POST /ai/query
```

---

# Run Project

```bash
uvicorn app.main:app --reload
```

---

# Future Improvements

* MCP integration
* ChromaDB vector search
* Docker support
* Deployment pipeline
* AI agent workflows

---

# Author

## Nigam Gouda

Backend & AI Engineer
