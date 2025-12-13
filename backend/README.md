# Backend - FastAPI with Prisma

This is the backend service for MLH Sidekick, built with FastAPI and Pydantic, using PostgreSQL with Prisma ORM.

## Prerequisites

- Python 3.12+
- UV (Python package manager)
- PostgreSQL database

## Setup

1. Install UV if you haven't already:
```bash
pip install uv
```

2. Install dependencies:
```bash
uv sync
```

3. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

4. Update the `DATABASE_URL` in `.env` with your PostgreSQL connection string.

5. Generate Prisma client:
```bash
uv run prisma generate
```

6. Run database migrations (when you have a running database):
```bash
uv run prisma db push
```

## Running the Server

Start the development server:
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive API docs (Swagger): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

## Linting

Run Pylint with the project settings in `.pylintrc`:

```bash
uv run pylint app
```

## Agents

This project also exposes ADK agents via the `adk api_server` command (see `railway.adk.json`). Agents live under `backend/agents/`:

- `sidekick_agent/root_agent`: general helper.
- `code_reviewer_agent/code_reviewer`: connects to the GitHub MCP server (read-only) and returns a structured JSON rubric for the provided code-sample questions. Requires `GITHUB_TOKEN` in the environment. The token is sent as a bearer header to `https://api.githubcopilot.com/mcp/` with toolsets `repos, issues, pull_requests, users, code_security, dependabot` in read-only mode.

Example start (local):

```bash
uv run adk api_server --host 0.0.0.0 --port 8001 agents
```

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
├── pyproject.toml       # Project metadata and dependencies
├── uv.lock             # Dependency lock file
└── README.md
```

## Technologies

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Prisma**: Next-generation ORM for Python
- **PostgreSQL**: Relational database
- **Uvicorn**: ASGI server for running the application
- **UV**: Fast Python package installer and resolver
