# MLH Sidekick

A monorepo project with a FastAPI backend and Next.js frontend.

## Project Structure

```
mlh-sidekick/
├── backend/          # FastAPI backend with Prisma ORM
│   ├── app/
│   ├── prisma/
│   └── requirements.txt
├── frontend/         # Next.js frontend with TypeScript
│   ├── app/
│   └── package.json
└── README.md
```

## Backend

The backend is built with:
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation and settings management
- **Prisma**: Type-safe ORM for PostgreSQL
- **PostgreSQL**: Database
- **UV**: Fast Python package manager

### Backend Setup

See [backend/README.md](./backend/README.md) for detailed setup instructions.

Quick start:
```bash
cd backend
uv sync
uv run prisma generate
uv run uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## Frontend

The frontend is built with:
- **Next.js 16**: React framework with TypeScript
- **React 19**: UI library
- **Tailwind CSS**: Utility-first CSS framework
- **TypeScript**: Type-safe JavaScript

### Frontend Setup

Quick start:
```bash
cd frontend
npm install
npm run dev
```

The app will be available at http://localhost:3000

## Development

### Prerequisites

- Python 3.12+
- UV (Python package manager)
- Node.js 20+
- PostgreSQL database (for backend)

### Running Both Services

In separate terminal windows:

1. Backend:
```bash
cd backend
uv run uvicorn app.main:app --reload
```

2. Frontend:
```bash
cd frontend
npm run dev
```

## License

MIT