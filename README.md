# DairyOS AI — Dairy Farm Management Backend

A production-ready backend system for managing dairy farm operations, built with FastAPI, MySQL, and AI-powered workflows using Gemini AI and RAG architecture.

---

## Overview

DairyOS AI provides a structured backend for dairy farm data management with an integrated AI layer that understands natural language queries, retrieves contextual knowledge, and executes backend operations through a tool-calling architecture.

---

## Features

### Backend
- JWT authentication with refresh token support
- Role-based access control (RBAC)
- Cow and milk record management APIs
- Pagination, sorting, and query parameter filtering
- SQLAlchemy ORM with Alembic migrations
- Modular service-layer architecture
- Input validation and structured exception handling
- Background task execution (email dispatch on user signup)

### AI & RAG
- Gemini AI integration for natural language query processing
- RAG pipeline with ChromaDB vector store and HuggingFace embedding models
- AI tool-calling workflows with dynamic function routing
- Intent-based backend execution
- AI-generated human-readable responses
- Real-time dairy analytics via natural language

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI, Python |
| ORM & Migrations | SQLAlchemy, Alembic |
| Database | MySQL |
| AI Model | Gemini AI |
| Vector Store | ChromaDB |
| Embeddings | HuggingFace Embedding Models |
| AI Architecture | Tool Calling, RAG, Function Routing |
| Auth | JWT, RBAC |
| Background Tasks | FastAPI BackgroundTasks |

---

## API Reference

### Authentication
```
POST /login
POST /refresh-token
```

### Farm Management
```
GET /cow?cow_tag=001
GET /cow/milkrecord?cow_tag=001&page=1&limit=5
```

### AI Query
```
POST /ai/query
```

---

## Example AI Queries

The `/ai/query` endpoint accepts natural language input and routes it to the appropriate backend function:

```
"today total milk"
"highest milk producing cow"
"monthly milk report"
"which cow gave highest milk this month"
```

The AI layer retrieves relevant context via RAG, interprets the intent, calls the appropriate tool, and returns a human-readable response.

---

## How the AI Layer Works

```
User Query (natural language)
        ↓
Gemini AI — intent understanding
        ↓
RAG — retrieves relevant farm context from ChromaDB
        ↓
Tool Calling — routes to the correct backend function
        ↓
Function executes against MySQL
        ↓
AI generates human-readable response
```

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/dairyos-ai.git
cd dairyos-ai
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 6. Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs at `http://localhost:8000/docs`.


---

## Roadmap

- [ ] MCP integration
- [ ] Docker support
- [ ] CI/CD deployment pipeline
- [ ] Multi-agent AI workflows
- [ ] Expanded RAG knowledge base for farm advisory queries

---

## Author

**Nigam Gouda**  
AI Backend Engineer