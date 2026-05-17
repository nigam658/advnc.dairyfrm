# Dairy Farm Management Backend API

Backend system for managing dairy farm operations using FastAPI and MySQL.

## Features

* JWT authentication and refresh tokens
* Role-based authorization
* Cow management APIs
* Milk record management
* Pagination and sorting
* SQLAlchemy ORM integration
* Query parameter filtering

## Tech Stack

* FastAPI
* Python
* MySQL
* SQLAlchemy
* Pydantic
* Alembic

## Example APIs

```http
POST /login
GET /cow?cow_tag=001
GET /cow/milkrecord?cow_tag=001&page=1&limit=5
```

## Run Project

```bash
uvicorn app.main:app --reload
```

## Future Improvements

* Dashboard analytics
* Docker support
* Deployment
* Report generation
* Inventory management

## Author

Nigam Gouda
