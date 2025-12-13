# Backend - FastAPI with Prisma

This is the backend service for MLH Sidekick, built with FastAPI and Pydantic, using PostgreSQL with Prisma ORM.

## Prerequisites

- Python 3.12+
- PostgreSQL database

## Setup

1. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

4. Update the `DATABASE_URL` in `.env` with your PostgreSQL connection string.

5. Generate Prisma client:
```bash
prisma generate
```

6. Run database migrations (when you have a running database):
```bash
prisma db push
```

## Running the Server

Start the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive API docs (Swagger): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI application and routes
├── prisma/
│   └── schema.prisma    # Database schema
├── .env.example         # Environment variables template
├── .gitignore
├── requirements.txt     # Python dependencies
└── README.md
```

## Technologies

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Prisma**: Next-generation ORM for Python
- **PostgreSQL**: Relational database
- **Uvicorn**: ASGI server for running the application
