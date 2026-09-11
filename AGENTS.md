# httpbinx Contributor Guide

## Project Overview

httpbinx is an HTTP request and response testing service built with FastAPI.
It follows a `src/` layout and supports Python 3.10 through 3.14.

## Repository Layout

- `src/httpbinx/main.py`: FastAPI application setup, middleware, static files, and router registration.
- `src/httpbinx/routers/`: Endpoint modules, grouped by HTTP behavior or feature.
- `src/httpbinx/schemas.py`: Pydantic request and response models.
- `src/httpbinx/helpers.py` and `constants.py`: Shared utilities and constants.
- `src/httpbinx/static/` and `templates/`: Assets and response templates.
- `tests/`: pytest test suite. The shared `client` fixture is defined in `tests/conftest.py`.

## Local Development

Activate the checked-in local environment before running Python commands:

```shell
source .venv/bin/activate
```

Synchronize the locked project and development dependencies when needed:

```shell
uv sync --locked
```

Run the service locally:

```shell
httpbinx server --host 0.0.0.0 --port 8000
```

## Verification

Run these checks before handing off Python changes:

```shell
pytest
ruff check .
ruff format --check .
```

Use Ruff to apply safe lint fixes or formatting when appropriate:

```shell
ruff check . --fix
ruff format .
```

## Implementation Guidelines

- Keep endpoint behavior in the relevant module under `src/httpbinx/routers/` and register new routers through the package router.
- Add or update endpoint tests in the matching `tests/test_*.py` module; use the shared FastAPI test client.
- Preserve public behavior compatible with the httpbin-style API unless the requested change intentionally alters it.
- Keep source code, comments, documentation, commit messages, issue text, and user-facing descriptions in English.
- Follow the existing Ruff configuration: 120-character lines, single quotes, and Google-style docstrings where docstrings are required.
- Avoid committing generated files, virtual environments, coverage output, or local-only guidance files.
