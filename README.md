# FastAPI Mastery & Production Backend Engineering

This workspace contains your complete roadmap, modular exercises, and production-grade capstone project designed to take you from fundamentals to **Senior Backend Engineer** level with FastAPI.

---

## 📖 Main Learning Guide & Exercises
👉 **[FASTAPI_MASTERY_ROADMAP_AND_EXERCISES.md](./FASTAPI_MASTERY_ROADMAP_AND_EXERCISES.md)**

---

## ⚡ Quick Start: Environment Setup

### 1. Create a Python Virtual Environment

Using standard Python virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Or using [`uv`](https://github.com/astral-sh/uv) (ultra-fast):
```bash
uv venv
source .venv/bin/activate
```

### 2. Core Dependencies
Install the standard production toolkit:
```bash
pip install fastapi "uvicorn[standard]" pydantic pydantic-settings \
            sqlalchemy asyncpg alembic pwdlib[argon2] pyjwt[crypto] \
            redis httpx pytest pytest-asyncio
```

---

## 🎯 Recommended Next Steps

1. Open [`FASTAPI_MASTERY_ROADMAP_AND_EXERCISES.md`](./FASTAPI_MASTERY_ROADMAP_AND_EXERCISES.md).
2. Start with **Module 1 (Modern Python Async & FastAPI Fundamentals)**.
3. As you work through each exercise, ask for hints, code reviews, or architectural guidance!
