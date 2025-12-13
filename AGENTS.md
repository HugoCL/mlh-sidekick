# MLH Sidekick - AI Agent Instructions

## Architecture Overview

Monorepo with FastAPI backend (Python 3.12+) and Next.js 16 frontend (React 19, TypeScript). Services run independently—backend on port 8000, frontend on 3000. No proxy layer exists; frontend makes direct HTTP calls to backend URLs.

## Critical Workflows

### Backend Development

- **Package manager**: Use UV, not pip. Commands: `uv sync`, `uv run <command>`
- **Database workflow**: Always run `uv run prisma generate` after schema changes, then `uv run prisma db push` (not migrations—this project uses push-based schema sync)
- **Start server**: `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- **Environment**: Requires `DATABASE_URL` in `.env` (PostgreSQL connection string)

### Frontend Development

- **Start dev server**: `npm run dev` (do NOT use yarn/pnpm unless package-lock.json is updated)
- **Tailwind**: v4 configuration is in [postcss.config.mjs](../frontend/postcss.config.mjs) via `@theme inline` blocks in [globals.css](../frontend/app/globals.css)—no separate tailwind.config.js
- **Fonts**: Geist Sans/Mono loaded in [layout.tsx](../frontend/app/layout.tsx) with CSS variable mapping

### Adding Features

1. **New backend endpoint**:
   - Add Pydantic models in [main.py](../backend/app/main.py) (or new module) for request/response validation
   - FastAPI uses type hints for automatic OpenAPI docs—leverage this
   - Example pattern: `@app.get("/health", response_model=HealthResponse)`
2. **Database model changes**:

   - Edit [schema.prisma](../backend/prisma/schema.prisma)
   - Run `uv run prisma generate` (creates Python client)
   - Run `uv run prisma db push` (syncs to PostgreSQL)
   - Import Prisma client: `from prisma import Prisma` (async/await pattern)

3. **Frontend API integration**:
   - No backend calls exist yet in the starter code
   - Fetch to `http://localhost:8000/...` from client/server components
   - Backend needs CORS setup for cross-origin requests (not configured by default)

## Project-Specific Conventions

- **Prisma client**: Uses `prisma-client-py` (not JS), with 5-level recursive type depth for relations
- **Backend structure**: Flat module structure in `app/`—no routers folder yet. Consider adding `app/routers/` if endpoints grow beyond 10-15
- **Frontend styling**: Tailwind utilities + CSS variables in `:root` and `@theme inline`. Dark mode via `prefers-color-scheme` media query
- **TypeScript**: Strict mode enabled (see [tsconfig.json](../frontend/tsconfig.json))
- **Next.js config**: Minimal—no custom webpack, image domains, or redirects defined yet

## Key Files

- Backend API entry: [backend/app/main.py](../backend/app/main.py)
- DB schema: [backend/prisma/schema.prisma](../backend/prisma/schema.prisma)
- Frontend root page: [frontend/app/page.tsx](../frontend/app/page.tsx)
- Global styles: [frontend/app/globals.css](../frontend/app/globals.css)

## Dependencies & Versions

- Backend: FastAPI 0.115.6, Pydantic 2.10, Prisma 0.15, uvicorn 0.34
- Frontend: Next.js 16.0.10, React 19.2, Tailwind 4 (PostCSS-based)
- ESLint 9 with Next.js config for linting

## Testing & Quality

No test framework configured yet. Backend has no linting setup. Frontend uses ESLint 9—run with `npm run lint`.

## Integration Points

- Database: PostgreSQL via Prisma ORM (async operations)
- API docs: Auto-generated at `/docs` (Swagger) and `/redoc` (ReDoc)
- Frontend ↔ Backend: Direct HTTP—no GraphQL, tRPC, or API middleware layer
