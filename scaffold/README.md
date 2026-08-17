# TickerTrack Scaffold

Starting point for the [ASSESSMENT-BRIEF.md](../ASSESSMENT-BRIEF.md). This scaffold gives you the folder structure, working infrastructure, complete database migrations, and realistic seed data — you implement the models, schemas, and route logic marked `TODO`.

## What's already done for you (do not modify)

- `alembic/versions/*.py` — all 6 tables, complete and correct
- `seed.py` — realistic seed data (managers across all 3 seniority levels, 5 tickers, 20 days of AAPL price history set up to produce a golden cross, portfolios with realistic target weights)
- `app/database.py` — SQLAlchemy engine/session setup
- `app/dependencies.py` — resolves the `X-Manager-Id` header to a `PortfolioManager` row (the "Login As" simulation)
- `app/error_handlers.py` — global exception handler
- `app/main.py` — FastAPI app wiring, router mounting, `/health` endpoint

## What you need to implement

- `app/models/*.py` — SQLAlchemy column definitions + relationships
- `app/schemas.py` — Pydantic request/response schemas
- `app/routers/*.py` — the actual endpoint logic, including every business rule described in the `TODO` comments — these map directly to the FR-N.N requirements in the brief, including the **per-manager portfolio isolation** requirement (FR-3.2), the **100%-total weight constraint** (FR-3.1/3.3), and **moving-average crossover detection** (FR-4.1)

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

createdb tickertrack_dev
cp .env.example .env

alembic upgrade head
python seed.py

uvicorn app.main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` for the auto-generated Swagger UI once your routes are implemented.

## Running tests

```bash
pytest
```

(You write these yourself per Deliverable 5 in the brief.)
