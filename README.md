# Job Tracker FastAPI

A REST API built with FastAPI and SQLite to manage and track job applications.

## What I Learned

Through this project I practiced:

- Building a REST API with FastAPI
- Using Pydantic models for request validation
- Structuring routes using APIRouter
- Using SQLite for persistent data storage
- Writing CRUD endpoints
- Writing SQL queries with SQLAlchemy
- Using response models and type hints
- Handling errors with HTTPException
- Using automatic Swagger documentation
- Organizing a backend project structure
- Working with status codes and API responses

## Features

- Create, read, update and delete job applications
- Filter applications by status
- SQLite database persistence
- Automatic request validation
- Automatic API documentation
- Response models
- Status code handling
- Modular route structure

## Technologies Used

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- Uvicorn

## How to Run

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python -m uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Applications

#### Get all applications

```text
GET /applications
```

Optional query parameter:

```text
?status=applied
```

#### Get one application

```text
GET /applications/<id>
```

#### Create application

```text
POST /applications
```

Example body:

```json
{
  "company": "Google",
  "position": "Backend Engineer",
  "status": "applied",
  "location": "Remote"
}
```

#### Update application

```text
PUT /applications/<id>
```

Example body:

```json
{
  "company": "Netflix",
  "position": "Python Developer",
  "status": "interview",
  "location": "Remote"
}
```

#### Delete application

```text
DELETE /applications/<id>
```