# 🚀 The Ultimate FastAPI Backend Engineering Mastery Roadmap & Exercises

Welcome to your structured training program to transition from beginner to **Senior/Production-Ready FastAPI Backend Engineer**.

This roadmap is split into **10 Progressive Modules** followed by a **Grand Capstone Project**. Each module contains **core theory**, **hands-on exercises** with clear requirements and acceptance criteria, and **pro-tips** representing modern industry standards.

---

## 🧭 Roadmap Overview

```
[Module 1: Async Python & FastAPI Core] ➔ [Module 2: Pydantic V2 & Data Validation]
                    ⬇
[Module 3: Dependency Injection (DI)]   ➔ [Module 4: Async SQLAlchemy 2.0 & Alembic]
                    ⬇
[Module 5: Security, Auth & RBAC]       ➔ [Module 6: Error Handling, Middleware & Logging]
                    ⬇
[Module 7: Caching & Background Queues] ➔ [Module 8: WebSockets & Streaming]
                    ⬇
[Module 9: Pytest & Automated TDD]     ➔ [Module 10: Docker, CI/CD & Observability]
                    ⬇
[🏆 Grand Capstone: Enterprise Multi-Tenant SaaS Backend]
```

---

## Recommended Project Structure (Clean / Modular Architecture)

When doing the exercises and capstone, follow this production-ready directory layout:

```text
fastapi_backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   └── items.py
│   │   │   └── api_router.py
│   │   └── deps.py              # Shared dependencies
│   ├── core/
│   │   ├── config.py            # Pydantic Settings
│   │   ├── database.py          # SQLAlchemy async engine & session
│   │   ├── security.py          # Password hashing, JWT helpers
│   │   └── exceptions.py        # Custom exceptions
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── base.py
│   │   └── user.py
│   ├── schemas/                 # Pydantic models (DTOs)
│   │   └── user.py
│   ├── crud/                    # Database access layer / Repositories
│   │   └── crud_user.py
│   ├── services/                # Business logic layer
│   │   └── user_service.py
│   ├── middlewares/             # Custom middlewares
│   └── main.py                  # App entrypoint
├── alembic/                     # Migrations
├── tests/                       # Pytest suite
│   ├── conftest.py
│   ├── test_api/
│   └── test_services/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env.example
├── pyproject.toml / requirements.txt
└── README.md
```

---

# 📚 Phase 1: Foundations & Core Architecture

---

### 🧩 Module 1: Modern Python Async & FastAPI Fundamentals

#### 🎯 Learning Objectives:
- Understand Python's `asyncio` event loop and why FastAPI uses `async def` vs `def` (threadpool offloading).
- Master Path, Query, Header, Cookie parameters, and Request Body parsing.
- Return structured responses using `Response`, `JSONResponse`, and Pydantic `response_model`.

#### 📝 Exercises:

##### Exercise 1.1: Async vs Sync Concurrency Benchmark
- **Task**: Create two endpoints in `app/main.py`:
  1. `/sync-task`: A standard `def` endpoint simulating heavy I/O using `time.sleep(2)`.
  2. `/async-task`: An `async def` endpoint simulating non-blocking I/O using `asyncio.sleep(2)`.
- **Validation**: Send 10 concurrent requests to both using `httpx` or `curl`. Observe how FastAPI manages threads for `def` versus concurrency in the event loop for `async def`.

##### Exercise 1.2: Advanced Parameter Validation & Metadata
- **Task**: Create an endpoint `GET /api/v1/products/search` that takes:
  - `q`: string, min length 3, max 50, required.
  - `price_min` & `price_max`: floats, greater than 0, where `price_max` is optional.
  - `categories`: list of strings passed as query parameters (e.g. `?categories=tech&categories=books`).
  - `X-Client-Version`: custom header required.
- **Validation**: Test with invalid inputs (e.g. `q` length < 3) and verify that FastAPI returns HTTP 422 with a structured error detail.

---

### 🧩 Module 2: Pydantic V2 & Data Validation Engine

#### 🎯 Learning Objectives:
- Master Pydantic V2 models, `@field_validator`, `@model_validator(mode='after')`, and `computed_field`.
- Strict typing, data coercion, serialization with `model_dump()`, `model_validate()`.
- Production configuration management using `pydantic-settings` with `.env` hierarchy.

#### 📝 Exercises:

##### Exercise 2.1: Rich User Registration Validator
- **Task**: Build a `UserCreate` schema with:
  - `email`: `EmailStr`.
  - `password`: string with at least 8 chars, 1 uppercase, 1 special character, and 1 number (custom `@field_validator`).
  - `confirm_password`: string. Use a `@model_validator` to ensure `password == confirm_password`.
  - `username`: lowercase alphanumeric only, stripped of whitespace.
- **Validation**: Create test payloads checking valid, mismatched passwords, and weak password rejections.

##### Exercise 2.2: Pydantic Settings with Environment Overrides
- **Task**: Create `app/core/config.py` using `pydantic_settings.BaseSettings`:
  - Fields: `PROJECT_NAME`, `ENVIRONMENT` (dev, staging, prod), `DATABASE_URL`, `REDIS_URL`, `ACCESS_TOKEN_EXPIRE_MINUTES`.
  - Read from `.env` file with environment variable fallback.
- **Validation**: Verify settings load accurately and reject startup if required fields are missing.

---

### 🧩 Module 3: FastAPI Dependency Injection (DI) Mastery

#### 🎯 Learning Objectives:
- Master `Depends()`, `Security()`, and hierarchical sub-dependencies.
- Understand `yield` dependencies for resource cleanup (DB sessions, file handles).
- Use Class-based dependencies for stateful filtering and pagination.

#### 📝 Exercises:

##### Exercise 3.1: Reusable Common Pagination Dependency
- **Task**: Create a reusable class `PaginationParams`:
  - Attributes: `page: int = 1`, `per_page: int = 20`, `sort_by: str = "id"`, `order: Literal["asc", "desc"] = "asc"`.
  - Enforce `per_page <= 100` and `page >= 1`.
  - Use `Depends(PaginationParams)` across multiple endpoints (`/users`, `/products`, `/orders`).
- **Validation**: Ensure endpoints automatically extract, validate, and convert pagination query parameters.

##### Exercise 3.2: Context-Managed Yield Dependency with Execution Timer
- **Task**: Write a dependency `get_request_context()` that:
  - Generates a unique `request_id` (UUID4).
  - Measures request processing time.
  - Yields a context dictionary `{"request_id": id, "started_at": timestamp}`.
  - Logs total duration after endpoint finishes execution (post-yield).

---

# 🗄️ Phase 2: Database Layer, ORM & Migrations

---

### 🧩 Module 4: Async SQLAlchemy 2.0 & Alembic

#### 🎯 Learning Objectives:
- Async database operations with `asyncpg` + PostgreSQL.
- Modern SQLAlchemy 2.0 syntax (`select()`, `insert()`, `update()`, `delete()`, `joinedload`, `selectinload`).
- Prevent N+1 queries using proper relationship loading.
- Database migrations with Alembic (auto-generation, rollbacks, data migrations).

#### 📝 Exercises:

##### Exercise 4.1: Database Engine & Async Session Lifecycle
- **Task**: Set up `app/core/database.py`:
  - Create `create_async_engine` with connection pooling (`pool_size=20`, `max_overflow=10`).
  - Create `async_sessionmaker`.
  - Implement `async def get_db() -> AsyncGenerator[AsyncSession, None]` with safe commit/rollback/close lifecycle.

##### Exercise 4.2: Relational Models (E-Commerce Schema)
- **Task**: Define SQLAlchemy models:
  - `User`: `id`, `email`, `hashed_password`, `is_active`, `created_at`.
  - `Order`: `id`, `user_id` (FK), `total_amount`, `status` (Enum: pending, paid, shipped, cancelled), `created_at`.
  - `OrderItem`: `id`, `order_id` (FK), `product_id` (FK), `quantity`, `unit_price`.
  - `Product`: `id`, `title`, `sku` (Unique), `price`, `stock_quantity`.
- **Validation**: Ensure bidirectional relationships (`relationship()`) are defined with `back_populates`.

##### Exercise 4.3: Alembic Async Migration Workflow
- **Task**:
  - Initialize Alembic (`alembic init -t async alembic`).
  - Configure `alembic/env.py` to use your `Base.metadata` and async engine.
  - Generate initial migration: `alembic revision --autogenerate -m "initial_schema"`.
  - Apply migration: `alembic upgrade head`.
  - Test downgrade: `alembic downgrade -1` and re-upgrade.

##### Exercise 4.4: Generic Async CRUD Repository Pattern
- **Task**: Build a generic `CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]` class with methods:
  - `get(db, id)`
  - `get_multi(db, skip, limit, filters)`
  - `create(db, obj_in)`
  - `update(db, db_obj, obj_in)`
  - `delete(db, id)`
- **Validation**: Inherit `CRUDUser` from `CRUDBase` and perform queries without raw SQL.

---

# 🔐 Phase 3: Security, Middleware & Architecture

---

### 🧩 Module 5: Authentication, Authorization & RBAC

#### 🎯 Learning Objectives:
- Password security with `pwdlib` / `passlib` (Argon2id or bcrypt).
- Stateful vs Stateless tokens (JWT Access Token + Refresh Token flow).
- Token revocation / blacklisting with Redis.
- Role-Based Access Control (RBAC) & Permission guards.

#### 📝 Exercises:

##### Exercise 5.1: Complete JWT Auth Flow (Access + Refresh)
- **Task**: Implement:
  - `POST /api/v1/auth/login`: Accepts `OAuth2PasswordRequestForm`, returns `{access_token, refresh_token, token_type}`.
  - `POST /api/v1/auth/refresh`: Accepts refresh token, validates it, and issues a new access token (Token Rotation).
  - `POST /api/v1/auth/logout`: Stores token JTI in Redis with TTL to invalidate immediately.

##### Exercise 5.2: Granular RBAC Dependency Guard
- **Task**:
  - Define Roles: `Role.ADMIN`, `Role.MANAGER`, `Role.CUSTOMER`.
  - Create a reusable dependency factory: `PermissionChecker(allowed_roles=[Role.ADMIN, Role.MANAGER])`.
  - Apply to protected routes (`DELETE /api/v1/users/{id}`, `POST /api/v1/products`).
- **Validation**: Non-admin users must receive HTTP 403 Forbidden with `{ "error": "Insufficient permissions" }`.

---

### 🧩 Module 6: Error Handling, Middleware & Observability

#### 🎯 Learning Objectives:
- Global Exception Handlers conforming to RFC 7807 (Problem Details for HTTP APIs).
- Custom ASGI Middlewares (Correlation ID, Rate Limiting, Request Logging).
- Structured logging with context propagation (`structlog`).

#### 📝 Exercises:

##### Exercise 6.1: Unified RFC 7807 Error Handling
- **Task**:
  - Create custom exception classes: `AppException`, `EntityNotFoundException`, `ConflictException`, `ForbiddenException`.
  - Register exception handlers on `FastAPI` instance to return uniform response:
    ```json
    {
      "type": "https://api.example.com/errors/not-found",
      "title": "Item Not Found",
      "status": 404,
      "detail": "Product with ID 42 was not found",
      "instance": "/api/v1/products/42",
      "request_id": "8e4d29b2-3c22-48df-b4a1-43283296fa2a"
    }
    ```

##### Exercise 6.2: Correlation ID & Request Timing Middleware
- **Task**: Create an ASGI middleware:
  - Checks incoming header `X-Request-ID` or generates a UUID.
  - Attaches `request_id` to `request.state`.
  - Sets `X-Request-ID` and `X-Process-Time-Ms` headers on the outgoing response.
  - Integrates with Python `logging` / `structlog` so all log records during the request include the `request_id`.

---

# ⚡ Phase 4: Performance, Async Queues & Realtime

---

### 🧩 Module 7: Redis Caching & Distributed Background Jobs

#### 🎯 Learning Objectives:
- Distributed caching strategies (Cache-Aside, TTL, Tag-based Invalidation).
- Background processing: Built-in `BackgroundTasks` vs Distributed Task Queues (Celery / ARQ / Taskiq).
- Handling race conditions with Redis distributed locks.

#### 📝 Exercises:

##### Exercise 7.1: Redis Cache-Aside Decorator for FastAPI
- **Task**:
  - Write a reusable decorator `@cache(ttl_seconds=300, key_prefix="product")`.
  - Store JSON responses in Redis.
  - If cache hit: return cached data immediately.
  - If cache miss: execute DB query, store in Redis, return result.
  - Implement cache invalidation when `PUT /api/v1/products/{id}` is called.

##### Exercise 7.2: Background Email & Report Queue with Celery / Redis
- **Task**:
  - Configure Celery with Redis broker and backend.
  - Create async background tasks:
    1. `send_welcome_email(user_id: int)`
    2. `generate_monthly_sales_csv(tenant_id: int)`
  - Trigger task from FastAPI endpoint and return HTTP 202 Accepted with `task_id`.
  - Provide endpoint `GET /api/v1/tasks/{task_id}/status` to check progress.

---

### 🧩 Module 8: WebSockets, SSE & Streaming

#### 🎯 Learning Objectives:
- FastAPI `WebSocket` endpoints and `WebSocketDisconnect` handling.
- Managing multiple active socket connections with a `ConnectionManager` (Rooms / Broadcast).
- Server-Sent Events (`siren` / `StreamingResponse`) for live event streaming.

#### 📝 Exercises:

##### Exercise 8.1: Multi-Room Realtime Chat with JWT Auth
- **Task**:
  - Build `ConnectionManager` that handles connections by `room_id`.
  - WebSocket endpoint `/ws/rooms/{room_id}?token=JWT_TOKEN`.
  - Verify JWT before accepting socket (`websocket.accept()`).
  - Broadcast messages sent by any client to all active clients in that specific room.
  - Handle abrupt client disconnects cleanly without memory leaks.

##### Exercise 8.2: Streaming Large Data Exports / LLM Token Stream
- **Task**:
  - Create an endpoint `GET /api/v1/analytics/export-stream` using `StreamingResponse`.
  - Stream 100,000 generated CSV rows chunk-by-chunk using an async generator without loading all rows into RAM at once.

---

# 🧪 Phase 5: Testing, DevOps & Production Readiness

---

### 🧩 Module 9: Production Testing & TDD (Pytest & TestContainers)

#### 🎯 Learning Objectives:
- Asynchronous testing using `pytest`, `pytest-asyncio`, and `httpx.AsyncClient`.
- Test Database isolation: Transaction rollback per test vs Isolated Test Containers.
- Mocking external APIs and services with `respx` / `unittest.mock`.
- Code coverage reporting (aiming for >85%).

#### 📝 Exercises:

##### Exercise 9.1: Pytest Test Fixture Harness
- **Task**: Set up `tests/conftest.py`:
  - `db_session` fixture: Creates tables on a test PostgreSQL instance (or SQLite in-memory), starts an async transaction, yields the session, and rolls back after each test so tests remain independent.
  - `client` fixture: `AsyncClient(transport=ASGITransport(app=app), base_url="http://test")` overriding `get_db` dependency with test session.
  - `auth_headers` fixture: Creates a test user and yields authorization header with valid bearer token.

##### Exercise 9.2: Complete Endpoint Integration Test Suite
- **Task**: Write full test cases for user registration and login:
  - Test successful registration (201 Created).
  - Test duplicate email registration (409 Conflict).
  - Test login with valid credentials (200 OK + JWT).
  - Test login with invalid credentials (401 Unauthorized).
  - Test accessing protected endpoint without token (401) and with valid token (200).

---

### 🧩 Module 10: Docker, CI/CD & Observability

#### 🎯 Learning Objectives:
- Multi-stage Docker builds for minimal, secure image sizes.
- Orchestration with Docker Compose (API, PostgreSQL, Redis, Celery, Prometheus, Grafana).
- Healthcheck endpoints (`/health/live`, `/health/ready`).
- Metrics collection using `prometheus-fastapi-instrumentator`.

#### 📝 Exercises:

##### Exercise 10.1: Production-Grade Multi-Stage Dockerfile
- **Task**: Write a `Dockerfile`:
  - Stage 1 (Builder): Install build dependencies, install python wheels.
  - Stage 2 (Runner): Minimal `python:3.12-slim`, non-root user (`appuser`), copy installed dependencies, run with Uvicorn.
  - Image size must be under 200MB.

##### Exercise 10.2: Full Docker Compose Development Stack
- **Task**: Create `docker-compose.yml` defining:
  - `web`: FastAPI application.
  - `db`: PostgreSQL 16 with health check.
  - `redis`: Redis 7 alpine.
  - `worker`: Celery worker instance sharing the same code.
  - Automatic database migrations executed before app starts.

---

# 🏆 The Capstone Project: "ShopPulse Pro" Enterprise Multi-Tenant E-Commerce SaaS

To prove you have mastered FastAPI at a professional level, build **ShopPulse Pro** — a production-ready, multi-tenant e-commerce backend platform.

```
+-----------------------------------------------------------------------------------+
|                                 ShopPulse Pro Architecture                        |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
                                   [ NGINX / Caddy ]
                                          │
                                          ▼
                             [ FastAPI Application Layer ]
            ┌─────────────────────────────┼─────────────────────────────┐
            │                             │                             │
            ▼                             ▼                             ▼
   [ Auth / RBAC Guard ]        [ Business Services ]         [ WebSocket Manager ]
            │                             │                             │
            ▼                             ▼                             ▼
   [ Async SQLAlchemy 2.0 ]      [ Redis Caching/Locks ]       [ Realtime Notifications ]
            │                             │
            ▼                             ▼
   [ PostgreSQL Database ]       [ Celery / Task Queue ] ────► [ Workers (PDF, Email, Stock) ]
```

### 📋 Capstone Requirements & Features

#### 1. Multi-Tenancy Architecture
- Each store/tenant has an isolated workspace (`tenant_id`).
- All queries automatically filter by tenant using SQLAlchemy query interceptors / session parameters.

#### 2. Authentication & Authorization (RBAC)
- Roles: `SuperAdmin`, `StoreAdmin`, `StoreManager`, `StoreCustomer`.
- Permissions: Granular scopes (e.g. `products:read`, `products:write`, `orders:refund`).
- Refresh token rotation + Redis token blacklist.

#### 3. High-Concurrency Inventory & Checkout System
- Optimistic / Pessimistic locking to prevent inventory overselling during flash sales.
- Database transactions wrapping order creation + inventory deduction.
- Idempotency key support for `POST /api/v1/orders/checkout` to prevent double charges on network retry.

#### 4. Asynchronous Workflow Engine
- Order status state machine: `PENDING` ➔ `PROCESSING` ➔ `SHIPPED` ➔ `DELIVERED` / `CANCELLED`.
- Background Celery tasks for:
  - Generating PDF Invoices and saving to S3 / local storage.
  - Firing Webhook notifications to external customer URLs with retry logic and HMAC signatures.

#### 5. Real-Time Order Dashboard
- WebSocket connection for store managers to receive live order updates and stock alerts.

#### 6. Redis Caching & Rate Limiting
- Cache hot product catalogs with automatic invalidation on product update.
- IP and API Key based rate limiter (e.g. 100 requests / minute) using Redis sliding window counter.

#### 7. Observability & Quality
- Prometheus metrics (`/metrics`) tracking latency histograms, request counts, and DB pool stats.
- 100% type annotations (`mypy` / `pyright` strict mode compliant).
- Comprehensive test suite in Pytest with ≥ 90% code coverage.
- Fully automated Docker Compose stack.

---

## 🛠️ Step-by-Step Suggested Learning Plan

| Step | Topic | Goal |
| :--- | :--- | :--- |
| **Week 1** | Modules 1 & 2 | Set up project with modern tooling (`uv` / `poetry`), Pydantic models, and settings. |
| **Week 2** | Modules 3 & 4 | Implement Async SQLAlchemy, migrations with Alembic, and the Repository pattern. |
| **Week 3** | Modules 5 & 6 | Build complete JWT Auth, RBAC guards, custom middlewares, and structured logging. |
| **Week 4** | Modules 7 & 8 | Add Redis caching, Celery background workers, and WebSockets. |
| **Week 5** | Modules 9 & 10 | Write comprehensive Pytest suites and build Docker multi-stage containers. |
| **Week 6+**| Capstone Project | Build **ShopPulse Pro** and deploy to a cloud VPS or Kubernetes cluster! |

---

## 🏁 Ready to Start?

You can start by creating the project skeleton right here in this repository! If you need help with any specific module, code template, or debugging along the way, just ask.
