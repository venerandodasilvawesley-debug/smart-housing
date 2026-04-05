# Smart Housing API — Copilot Instructions

FastAPI + PostgreSQL REST API for managing employee housing (alojamentos de colaboradores).

## Commands

```bash
# Run the app locally
uvicorn main:app --reload

# Run with Docker (recommended)
docker compose up --build

# Run all tests
pytest tests/ -v

# Run a single test file
pytest tests/test_alocacoes.py -v

# Run a single test by name
pytest tests/test_alocacoes.py::test_quarto_cheio_bloqueado -v

# Database migrations
alembic upgrade head   # apply migrations
alembic revision --autogenerate -m "description"  # generate migration
```

## Architecture

The app follows a layered pattern:

```
routes/ → crud.py / services/ → repositories/base.py → models.py
```

- **`app/routes/`** — FastAPI routers (one file per resource). Only handle HTTP concerns; delegate to `crud` or `services`.
- **`app/crud.py`** — Direct SQLAlchemy queries for simple CRUD. Business logic that requires HTTP exceptions (like blocking deletes when active allocations exist) also lives here.
- **`app/services/alocacao_service.py`** — Business logic for allocations (capacity checks, occupancy tracking). Complex operations that update multiple models go here.
- **`app/repositories/base.py`** — Generic reusable queries (`get_all`, `get_by_id`, `save`, `delete`) plus a few domain-specific queries. Used by `services/`.
- **`app/models.py`** — SQLAlchemy ORM models (all in one file).
- **`app/schemas.py`** — Pydantic v2 schemas (all in one file). Each resource has `Base`, `Create`, `Update`, and `Read` variants.
- **`app/auth.py`** — JWT creation/validation and FastAPI dependency functions (`get_current_user`, `require_admin`).
- **`app/database.py`** — Engine, `SessionLocal`, `Base`, and the `get_db` dependency.
- **`main.py`** — App entry point: registers routers, middleware, and global exception handlers.

## Key Conventions

### Auth dependencies on routes
- `Depends(get_current_user)` → requires any authenticated user (assigned to `_`)
- `Depends(require_admin)` → requires `role == "admin"` (also assigned to `_`)
- DELETE endpoints always require `require_admin`; GET/POST/PUT use `get_current_user`

### Pydantic v2
Schemas use `model_dump()` (not `.dict()`), `model_config = {"from_attributes": True}` on Read schemas, and `@model_validator(mode="after")` for cross-field validation.

### Update pattern
All `update_*` functions in `crud.py` use `data.model_dump(exclude_none=True)` + `setattr` to apply partial updates without overwriting unset fields.

### Occupancy tracking
`Quarto.ocupacao_atual` is maintained manually: incremented in `alocacao_service.alocar_colaborador` and decremented in `alocacao_service.desalocar_colaborador`. Do not update it directly from routes.

### Delete guards
Deleting a `Colaborador` or `Quarto` with an active allocation (`data_saida == None`) raises HTTP 409. This is enforced in `crud.py`.

### Tests
- Tests use SQLite in-memory (`test.db`) via `conftest.py`, which overrides `get_db` with `dependency_overrides`.
- `reset_db` fixture (autouse) creates and drops all tables around each test.
- Use the `auth(token)` helper from `conftest.py` to build auth headers.
- Each test file has local helper functions (e.g., `_criar_quarto`, `_criar_colaborador`) to set up prerequisites.

### Environment
Required env vars: `DATABASE_URL`, `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`. See `.env.example`. Tests do not need `DATABASE_URL` (SQLite is hardcoded in conftest).

### Manutencao status values
Valid values are `"Aberto"`, `"Em andamento"`, `"Fechado"` (enforced via `Literal` in schemas).
