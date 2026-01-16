# HabbotConnect
Backend assessment project built with FastAPI and MongoDB.

## Overview
HabbotConnect provides a REST API for authentication and employee management. It is a FastAPI app with MongoDB as the data store and JWT-based auth.

## Features
- Auth: login and signup
- Employees: create, list, fetch, update, delete
- Health endpoint and API docs

## Tech Stack
- API: FastAPI, Starlette, Uvicorn
- Database: MongoDB (pymongo, motor)
- Auth: JWT (PyJWT, python-jose), passlib
- Tooling: pytest, ruff, black, isort, pre-commit

## Project Structure
```
apps/
  fastapi/
    src/                 FastAPI app entrypoint
    platform/modules/    API modules (auth, core, employees)
libs/
  utils/                 shared utilities (config, db, logging)
tests/                   pytest tests
```

## Prerequisites
- Python 3.12+ recommended
- MongoDB instance available

## Setup (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item example.env .env
```

## Configuration
Edit `.env` with your settings:
- `MONGO_URI`
- `MONGO_DATABASE_NAME`
- `SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REFRESH_TOKEN_EXPIRE_DAYS`
- `ALGORITHM`
- `FASTAPI_APP_ENVIRONMENT` (default: development)
- `FASTAPI_APP_HOST` (default: 127.0.0.1)
- `FASTAPI_APP_PORT` (default: 5000)

## Run the Backend (Development)
```powershell
python -m uvicorn apps.fastapi.src:app --reload --host 127.0.0.1 --port 5000
```
API docs: `http://127.0.0.1:5000/docs`

## Run the Backend (Production)
Set `FASTAPI_APP_ENVIRONMENT=production` and `GUNICORN_CONFIG_PATH` in `.env`, then start via your process manager using gunicorn. The app entry is `apps.fastapi.src:app`.

## Testing
```powershell
pytest
```

## Linting and Formatting
```powershell
ruff check .
black .
isort .
```

## Pre-commit (Optional)
```powershell
pre-commit install
pre-commit run --all-files
```

## API Notes
- Base path: `/api`
- Health: `/api/health`
- Auth: `/api/auth/login`, `/api/auth/signup`
- Employees: `/api/employees`

## Troubleshooting
- `.env file not found`: Copy `example.env` to `.env` and fill required values.
- Mongo connection errors: Verify `MONGO_URI` and network access to your MongoDB instance.
- Auth failures: Check `SECRET_KEY` and token settings in `.env`.
