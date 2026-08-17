# Assessment Brief — TickerTrack Portfolio Monitor
### Python Project | FastAPI · SQLAlchemy · Alembic · PostgreSQL · pandas/openpyxl
**Duration:** 5 Days | **Trainee Name:** MUHAMAD AMIR RIDWAN BIN RAZUIN

---

## 1. Background

**Northgate Asset Management** runs several equity portfolios, each owned by a portfolio manager (PM). PMs need to track daily prices for the tickers in their own portfolio, get notified when a short-term/long-term moving-average crossover signals a potential trend change, and produce an Excel report for the investment committee. The firm has asked for an internal tool — **TickerTrack** — to manage PM accounts, record daily price snapshots, maintain each PM's portfolio holdings (with target weights), detect crossover signals, and generate the committee report.

PMs use TickerTrack daily to: register/manage PM accounts, log daily closing prices and volume for tickers, manage their own portfolio's holdings and target weights, review crossover signals for their tickers, and generate an Excel report of their portfolio's performance.

## 2. Users of the System

There is **one user role**: **Portfolio Manager (PM)**. Full authentication is **not required**.

Every request that creates, modifies, or scopes data must include an `X-Manager-Id` header:

```
X-Manager-Id: 2
```

Your API must resolve this to a PM record and use it to scope portfolio-holding reads/writes to that PM only, and to gate report generation by `seniority` (see FR-4). Reject the request if the header is missing, the PM doesn't exist, or the PM is inactive.

## 3. Functional Requirements

### FR-1: Portfolio Manager Account Management

- **FR-1.1** — `POST /managers` creates a PM (`name`, `email`, `seniority`).
  **Business rule:** `email` must be unique — return `400` if taken.
- **FR-1.2** — `GET /managers` lists all PMs, paginated.
- **FR-1.3** — `GET /managers/{id}` returns one PM or `404`.
- **FR-1.4** — `PUT /managers/{id}` updates a PM's fields.
- **FR-1.5** — `DELETE /managers/{id}` is not supported (deactivate instead, so historical holdings/signals/reports stay valid). Return `405`.

### FR-2: Ticker Reference & Price Snapshots

- **FR-2.1** — `GET /tickers` lists the reference table of tracked tickers (seeded; read-only in this assessment).
- **FR-2.2** — `POST /tickers/{id}/prices` records a new daily price snapshot (`price`, `volume`, `captured_at`, `source`).
  **Business rule:** `price` must be `> 0`; `volume` must be `>= 0`.
  **Business rule:** `captured_at` must be chronologically after the ticker's most recent snapshot — reject out-of-order backfills with `400`.
- **FR-2.3** — `GET /tickers/{id}/prices` lists price history, paginated, most recent first.

### FR-3: Portfolio Holdings (scoping + aggregate constraint — the domain-unique concept)

- **FR-3.1** — `POST /holdings` adds a ticker to the requesting PM's (`X-Manager-Id`) portfolio with a `target_weight_pct`.
  **Business rule:** a PM cannot add the same ticker to their portfolio twice — return `400` ("already in your portfolio").
  **Business rule (unique aggregate rule — not present in the other domain variants):** the sum of `target_weight_pct` across a PM's **entire** portfolio (existing holdings + the new one) must not exceed `100`. Return `400` ("total target weight would exceed 100%") if it would.
- **FR-3.2** — `GET /holdings` returns **only the requesting PM's own portfolio** — Manager A's holdings must never appear when Manager B calls this with their own `X-Manager-Id` (isolation test, same pattern as the other domain variants' watchlist/agent scoping, applied here to holdings).
- **FR-3.3** — `PUT /holdings/{ticker_id}` updates the `target_weight_pct` for a ticker already in the PM's portfolio.
  **Business rule:** the same 100%-total constraint from FR-3.1 applies to updates — recompute the total excluding the old value for that ticker before checking.
- **FR-3.4** — `DELETE /holdings/{ticker_id}` removes a ticker from the requesting PM's portfolio. Removing something not held returns `404`.

### FR-4: Crossover Signals & Report Generation

- **FR-4.1** — Whenever a new price snapshot is recorded (FR-2.2) and the ticker has **at least 20** price snapshots, auto-compute a 5-day moving average and a 20-day moving average. If the 5-day average crosses from below to above the 20-day average, create a `CrossoverSignal` with `signal_type = golden_cross`; if it crosses from above to below, create one with `signal_type = death_cross`.
  **Business rule:** `signal_type` is always server-computed from the actual moving averages — there is no endpoint that lets a client set it directly.
  **Business rule:** if fewer than 20 snapshots exist yet for the ticker, no signal is computed (not an error — just nothing to detect yet).
- **FR-4.2** — `GET /signals` lists signals, filterable by `?ticker_id=`, paginated.
- **FR-4.3** — `POST /reports` generates an Excel report for the requesting PM's (`X-Manager-Id`) **current portfolio only** over a date range, including raw prices, 5-day/20-day moving averages, % change, target weights, and highlighted crossover-signal rows.
  **Business rule:** the PM's portfolio must contain **at least one holding**, or return `400` ("add a holding to your portfolio first").
  **Business rule:** a ticker with fewer than 20 snapshots in range is included in the report with its raw prices but a note that moving averages/signals aren't yet available, rather than excluding it or failing the request.
- **FR-4.4** — `GET /reports/{id}/download` streams the generated `.xlsx`. Return `404` if the file is missing.

## 4. Non-Functional Requirements

- **NFR-1** — Correct HTTP status codes: `200`, `201`, `400`, `404`, `405`, `500`.
- **NFR-2** — Pagination on all list endpoints once records exceed 20.
- **NFR-3** — Input validation via Pydantic with descriptive messages.
- **NFR-4** — Schema managed via **Alembic migrations only** — no `create_all()`.
- **NFR-5** — No hard-coded credentials; connection string and any keys via `.env`.
- **NFR-6** — Network/data-source failures when fetching price data return a clean `502`/`503`, never an unhandled exception.

## 5. Technical Constraints

| Layer | Technology | Notes |
|-------|-----------|-------|
| API framework | FastAPI | |
| ORM | SQLAlchemy 2.x | |
| Migrations | Alembic | |
| Database | PostgreSQL 16 | |
| DB driver | `psycopg2-binary` | |
| Data processing | `pandas` (optional) + `openpyxl` | |
| Price source | `requests` (JSON API preferred, e.g. a free-tier market-data API) | |
| Testing | `pytest` + FastAPI `TestClient` | |
| Config | `python-dotenv` | |

**You may NOT use:** SQLite or any non-PostgreSQL database · `create_all()` in place of Alembic · raw string-interpolated SQL · hardcoded credentials/keys · a real auth library (the `X-Manager-Id` header is the required simulation).

## 6. What You Are Given

Same lightweight scaffold approach as the other domain variants: `requirements.txt`, `.env.example`, an initialized empty `alembic/` folder, and a stub `app/main.py` with no routes implemented. The full TODO-annotated scaffold (Component 3) is a follow-up build — see `python-training-revised.md` §4; build your own project structure from this brief's Data Model/API reference in the meantime.

## 7. Deliverables

1. GitHub repository link.
2. Working FastAPI app + Alembic migrations, runnable from a clean clone.
3. `requirements.txt`.
4. Portfolio-holding scoping logic, crossover-signal computation, and Excel report generation, with unit tests for the pure business-logic functions (moving averages, crossover detection, weight-total validation).
5. API tests covering the isolation test in FR-3.2, the 100%-total constraint in FR-3.1/3.3, and the other business rules in Section 3.
6. `README.md` — setup, API docs, portfolio/report usage, design notes.
7. `NOTES.md` — reflection on what was hardest and any known limitations.

## 8. Data Model Reference

### `portfolio_managers`

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | Primary key |
| name | VARCHAR(100) | Not null |
| email | VARCHAR(150) | Not null, unique |
| seniority | ENUM | `analyst`, `associate`, `principal` — not null |
| active | BOOLEAN | Not null, default `true` |
| created_at | TIMESTAMP | Not null, default now |

### `tickers` (reference table, seeded)

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | Primary key |
| symbol | VARCHAR(10) | Not null, unique |
| company_name | VARCHAR(150) | Not null |
| sector | VARCHAR(50) | Not null |
| is_active | BOOLEAN | Not null, default `true` |

### `price_snapshots`

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | Primary key |
| ticker_id | INTEGER | FK → `tickers.id`, not null |
| price | DECIMAL(12,4) | Not null, must be `> 0` |
| volume | BIGINT | Not null, must be `>= 0` |
| captured_at | TIMESTAMP | Not null; chronologically after the previous snapshot for this ticker |
| source | VARCHAR(100) | Not null |

### `portfolio_holdings` (junction table — scoping + aggregate constraint)

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | Primary key |
| manager_id | INTEGER | FK → `portfolio_managers.id`, not null |
| ticker_id | INTEGER | FK → `tickers.id`, not null |
| target_weight_pct | DECIMAL(5,2) | Not null; sum per manager must not exceed 100 |
| added_at | TIMESTAMP | Not null, default now |
| | | Unique constraint on (`manager_id`, `ticker_id`) |

### `crossover_signals`

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | Primary key |
| ticker_id | INTEGER | FK → `tickers.id`, not null |
| price_snapshot_id | INTEGER | FK → `price_snapshots.id`, not null |
| signal_type | ENUM | `golden_cross`, `death_cross` — not null, server-computed only |
| short_ma | DECIMAL(12,4) | Not null — the 5-day average at detection time |
| long_ma | DECIMAL(12,4) | Not null — the 20-day average at detection time |
| detected_at | TIMESTAMP | Not null, default now |

### `reports`

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | Primary key |
| manager_id | INTEGER | FK → `portfolio_managers.id`, not null |
| date_from | DATE | Not null |
| date_to | DATE | Not null |
| filename | VARCHAR(200) | Not null |
| row_count | INTEGER | Not null |
| generated_at | TIMESTAMP | Not null, default now |

## 9. API Endpoint Reference

| Method | Path | Description |
|---|---|---|
| POST | `/managers` | Create a portfolio manager |
| GET | `/managers` | List managers (paginated) |
| GET | `/managers/{id}` | Get one manager |
| PUT | `/managers/{id}` | Update a manager |
| DELETE | `/managers/{id}` | Not supported — returns 405 |
| GET | `/tickers` | List tracked tickers |
| POST | `/tickers/{id}/prices` | Record a new price snapshot (auto-detects crossover signals) |
| GET | `/tickers/{id}/prices` | List price history (paginated) |
| POST | `/holdings` | Add a ticker to the requesting manager's portfolio |
| GET | `/holdings` | List the requesting manager's own portfolio only |
| PUT | `/holdings/{ticker_id}` | Update target weight for a held ticker |
| DELETE | `/holdings/{ticker_id}` | Remove a ticker from the requesting manager's portfolio |
| GET | `/signals` | List crossover signals (filterable, paginated) |
| POST | `/reports` | Generate an Excel report for the requesting manager's portfolio |
| GET | `/reports` | List generated reports (paginated) |
| GET | `/reports/{id}/download` | Download the generated `.xlsx` file |

## 10. Evaluation Rubric

> As with the other domain variants in this program, Phase 4 is redefined from "Frontend" to **"Data Pipeline & Reporting"** since this assessment is API-only.

| Phase | Domain | Max marks |
|-------|--------|-----------|
| 1 | Structure & Configuration | 8 |
| 2 | Database & Models | 20 |
| 3 | API / Backend (managers, tickers, holdings, signals) | 30 |
| 4 | Data Pipeline & Reporting (price ingestion, crossover detection, moving averages, Excel export) | 30 |
| 5 | Code Quality | 12 |
| **Total** | | **100** |

**Pass mark: 60/100.**

---

*Domain variant of the FXPulse brief ([assessment-treasury](../assessment-treasury/ASSESSMENT-BRIEF.md)) and the Commodity Watch brief ([assessment-commodity](../assessment-commodity/ASSESSMENT-BRIEF.md)) — same rubric weights and technical constraints, different entity, scoping concept (per-manager portfolio isolation **plus** a 100%-total aggregate constraint unique to this domain), and business rule shape (moving-average crossover detection instead of a simple threshold-breach alert). See [python-training-revised.md](../python-training-revised.md) and [python-learning-guide.md](../python-learning-guide.md) for the surrounding program context.*
