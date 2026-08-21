# TickerTrack Portfolio Monitor

TickerTrack is a FastAPI-based portfolio monitoring API developed as part of the Python backend assessment for Northgate Asset Management.

The application allows Portfolio Managers (PMs) to:

* Manage portfolio manager accounts
* View tracked equity tickers
* Record daily price snapshots
* Maintain portfolio holdings and target weights
* Enforce a 100% portfolio target-weight limit
* Isolate holdings by Portfolio Manager
* Detect 5-day / 20-day moving-average crossover signals
* View crossover signals
* Generate Excel portfolio reports
* Download generated Excel reports

The implementation uses PostgreSQL, SQLAlchemy, Alembic, FastAPI, Pydantic and openpyxl.

---

## 1. Technology Stack

| Component       | Technology                        |
| --------------- | --------------------------------- |
| API Framework   | FastAPI 0.111.0                   |
| ORM             | SQLAlchemy 2.0.30                 |
| Database        | PostgreSQL 16                     |
| Database Driver | psycopg2-binary 2.9.9             |
| Migrations      | Alembic 1.13.1                    |
| Validation      | Pydantic 2.7.1                    |
| Data Processing | pandas 2.2.2                      |
| Excel Reporting | openpyxl 3.1.2                    |
| HTTP Client     | requests 2.32.3                   |
| Testing         | pytest 8.2.0 + FastAPI TestClient |
| Configuration   | python-dotenv                     |

---

## 2. Project Structure

```text
scaffold/
│
├── app/
│   ├── business_logic/
│   │   ├── __init__.py
│   │   ├── moving_average.py
│   │   ├── crossover.py
│   │   └── portfolio.py
│   │
│   ├── models/
│   │   ├── crossover_signal.py
│   │   ├── portfolio_holding.py
│   │   ├── portfolio_manager.py
│   │   ├── price_snapshot.py
│   │   ├── report.py
│   │   └── ticker.py
│   │
│   ├── routers/
│   │   ├── holdings.py
│   │   ├── managers.py
│   │   ├── reports.py
│   │   ├── signals.py
│   │   └── tickers.py
│   │
│   ├── database.py
│   ├── dependencies.py
│   ├── error_handlers.py
│   ├── main.py
│   └── schemas.py
│
├── alembic/
│   ├── versions/
│   │   ├── 0001_create_portfolio_managers.py
│   │   ├── 0002_create_tickers.py
│   │   ├── 0003_create_price_snapshots.py
│   │   ├── 0004_create_portfolio_holdings.py
│   │   ├── 0005_create_crossover_signals.py
│   │   └── 0006_create_reports.py
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│   ├── unit/
│   │   ├── test_moving_average.py
│   │   ├── test_crossover.py
│   │   └── test_portfolio.py
│   │
│   └── api/
│       ├── conftest.py
│       ├── test_managers.py
│       ├── test_prices.py
│       ├── test_holdings.py
│       ├── test_signals.py
│       └── test_reports.py
│
├── reports/
├── seed.py
├── requirements.txt
├── alembic.ini
├── .env.example
├── .gitignore
├── README.md
├── NOTES.md
└── run_migrations.py
```

---

## 3. Prerequisites

### Local Development

Install:

* Python 3.12
* PostgreSQL 16
* Git
* Postman or another API client

### Docker

For the containerized version, only Docker Desktop is required.

---

## 4. Local Development Setup

### 4.1 Clone the Repository

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd scaffold
```

---

### 4.2 Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

Verify:

```powershell
python --version
```

Expected:

```text
Python 3.12.x
```

---

### 4.3 Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 5. PostgreSQL Setup

Create a PostgreSQL database named:

```text
tickertrack_dev
```

Example using `psql`:

```powershell
psql -U postgres
```

Then:

```sql
CREATE DATABASE tickertrack_dev;
```

The application connection is configured through `.env`.

---

## 6. Environment Variables

Create `.env` from `.env.example`.

Example:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/tickertrack_dev
```

Do not commit `.env` to GitHub.

`.gitignore` excludes the real environment file.

---

## 7. Database Migrations

The assessment scaffold provides all six database migrations.

The migration files under:

```text
alembic/versions/
```

are provided by the assessment and were kept unchanged.

Due to the PostgreSQL ENUM creation behavior in the supplied scaffold with the pinned SQLAlchemy version, a small local compatibility runner is provided:

```text
run_migrations.py
```

Run migrations with:

```powershell
python run_migrations.py
```

After successful migration, verify:

```powershell
alembic current
```

The database should be at revision:

```text
0006
```

The resulting tables are:

```text
portfolio_managers
tickers
price_snapshots
portfolio_holdings
crossover_signals
reports
```

---

## 8. Seed Data

The scaffold includes realistic seed data.

Run:

```powershell
python seed.py
```

The seed includes:

* Portfolio managers across the supported seniority levels
* Five tracked tickers
* Twenty days of AAPL price history
* Existing portfolio holdings with target weights
* Data designed to support crossover testing

---

## 9. Run the API

Start FastAPI with:

```powershell
uvicorn app.main:app --reload --port 8000
```

API:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## 10. Authentication / Manager Scoping

Full authentication is not required for this assessment.

The application uses the required:

```http
X-Manager-Id: <manager_id>
```

header as the "Login As" simulation.

Example:

```http
X-Manager-Id: 2
```

The provided `app/dependencies.py` resolves the header to a `PortfolioManager`.

For portfolio-scoped operations, the requesting manager is used to isolate the data.

The client does not submit `manager_id` in holding creation requests.

---

## 11. API Endpoints

### Portfolio Managers

| Method | Endpoint                 | Description                          |
| ------ | ------------------------ | ------------------------------------ |
| POST   | `/managers`              | Create a manager                     |
| GET    | `/managers`              | List managers                        |
| GET    | `/managers/{manager_id}` | Get a manager                        |
| PUT    | `/managers/{manager_id}` | Update/deactivate a manager          |
| DELETE | `/managers/{manager_id}` | Returns 405; deletion is unsupported |

Example create request:

```http
POST /managers
Content-Type: application/json
```

```json
{
  "name": "Test Manager",
  "email": "test.manager@example.com",
  "seniority": "associate"
}
```

---

### Tickers

| Method | Endpoint                      | Description                |
| ------ | ----------------------------- | -------------------------- |
| GET    | `/tickers/`                   | List seeded active tickers |
| POST   | `/tickers/{ticker_id}/prices` | Record a price snapshot    |
| GET    | `/tickers/{ticker_id}/prices` | List price history         |

Example price request:

```json
{
  "price": 230.50,
  "volume": 1250000,
  "captured_at": "2026-08-18T10:00:00",
  "source": "manual"
}
```

Business rules:

* `price` must be greater than 0
* `volume` must be greater than or equal to 0
* `captured_at` must be later than the latest snapshot for the ticker

---

### Portfolio Holdings

| Method | Endpoint                | Description                              |
| ------ | ----------------------- | ---------------------------------------- |
| POST   | `/holdings/`            | Add holding to current manager portfolio |
| GET    | `/holdings/`            | List current manager's holdings          |
| PUT    | `/holdings/{ticker_id}` | Update target weight                     |
| DELETE | `/holdings/{ticker_id}` | Remove holding                           |

All holding operations use:

```http
X-Manager-Id: <manager_id>
```

#### Portfolio isolation

A manager can only access their own portfolio holdings.

For example:

```text
Manager A → AAPL, MSFT
Manager B → NVDA
```

Manager B must never receive Manager A's holdings.

#### Aggregate weight constraint

The total target weight for a manager's complete portfolio cannot exceed 100%.

For a new holding:

```text
existing total + new weight <= 100%
```

For an update:

```text
current total - old weight + new weight <= 100%
```

Attempting to exceed the limit returns:

```text
400 Bad Request
```

---

### Signals

| Method | Endpoint                   | Description              |
| ------ | -------------------------- | ------------------------ |
| GET    | `/signals/`                | List crossover signals   |
| GET    | `/signals/?ticker_id={id}` | Filter signals by ticker |

Pagination is supported using:

```text
?page=1&page_size=20
```

---

### Reports

| Method | Endpoint                        | Description                      |
| ------ | ------------------------------- | -------------------------------- |
| POST   | `/reports/`                     | Generate Excel report            |
| GET    | `/reports/`                     | List reports for current manager |
| GET    | `/reports/{report_id}/download` | Download generated Excel file    |

Example:

```json
{
  "date_from": "2026-07-01",
  "date_to": "2026-08-18"
}
```

Reports use the requesting manager's current portfolio.

---

## 12. Moving Average Logic

The application calculates:

```text
5-day moving average
20-day moving average
```

The calculation is implemented as pure business logic in:

```text
app/business_logic/moving_average.py
```

For a window of five:

```text
MA5 = sum(last 5 prices) / 5
```

For a window of twenty:

```text
MA20 = sum(last 20 prices) / 20
```

Fewer than the required number of observations results in an unavailable moving-average value.

Financial values use `Decimal` to remain consistent with PostgreSQL `NUMERIC` columns.

---

## 13. Crossover Detection

Crossover detection is implemented in:

```text
app/business_logic/crossover.py
```

### Golden Cross

A golden cross occurs when:

```text
Previous:
5MA <= 20MA

Current:
5MA > 20MA
```

The server creates:

```text
signal_type = golden_cross
```

### Death Cross

A death cross occurs when:

```text
Previous:
5MA >= 20MA

Current:
5MA < 20MA
```

The server creates:

```text
signal_type = death_cross
```

The client cannot directly choose the signal type.

Signals are created automatically during price snapshot processing.

---

## 14. Excel Reporting

Reports are generated using `openpyxl`.

The workbook contains a:

```text
Portfolio Report
```

worksheet with:

```text
Date
Ticker
Price
5-Day MA
20-Day MA
% Change
Target Weight %
Signal
Note
```

Crossover rows are highlighted.

For a ticker with fewer than 20 snapshots within the requested reporting range:

* Raw prices are still included
* The ticker is not excluded
* Moving averages/signals are marked as unavailable
* A note is included in the report

Generated files are saved under:

```text
reports/
```

---

## 15. Pagination

List endpoints support pagination using:

```text
?page=1&page_size=20
```

Pagination is implemented for:

```text
GET /managers
GET /tickers/{ticker_id}/prices
GET /signals
GET /reports
```

---

## 16. Validation and Error Handling

Pydantic handles request validation such as:

```text
Invalid email
Invalid seniority
price <= 0
volume < 0
target weight outside valid range
```

Business rules are handled within the application logic.

Examples:

```text
400
Invalid business rule

401
Unknown X-Manager-Id

404
Requested record/file not found

405
Manager deletion not supported

422
FastAPI/Pydantic request validation failure
```

External/network failures from a future market-data integration should be converted into appropriate 502/503 responses rather than unhandled exceptions.

---

## 17. Testing

Run all tests:

```powershell
pytest -v
```

Run only unit tests:

```powershell
pytest tests\unit -v
```

Run only API tests:

```powershell
pytest tests\api -v
```

Run with a concise summary:

```powershell
pytest -q
```

The automated tests cover:

### Unit Tests

* Moving-average calculation
* Golden-cross detection
* Death-cross detection
* No-crossover scenarios
* Portfolio total-weight validation
* Portfolio update-weight validation

### API Tests

* Manager creation
* Duplicate manager email
* Manager update
* Manager deactivation
* Unsupported manager deletion
* Ticker listing
* Price creation
* Invalid price
* Invalid volume
* Out-of-order snapshots
* Price pagination
* Holding creation
* Duplicate holdings
* Manager portfolio isolation
* 100% portfolio-weight constraint
* Holding updates
* Holding deletion
* Signal filtering
* Report generation
* Report scoping
* Report download
* Missing report file
* Missing `X-Manager-Id`
* Inactive-manager behavior

---

## 18. Postman

For manual API testing, use:

```text
Base URL:
http://127.0.0.1:8000
```

Recommended environment variables:

```text
base_url
manager_id
manager_a_id
manager_b_id
ticker_id
aapl_ticker_id
report_id
```

Example scoped request:

```http
GET {{base_url}}/holdings/
X-Manager-Id: {{manager_a_id}}
```

---

## 19. Docker

The project includes a Dockerized environment as a bonus task.

The Docker setup contains two services:

```text
FastAPI Application
        |
        | Docker Network
        |
PostgreSQL Database
```

### FastAPI Container

The `Dockerfile`:

* Uses Python 3.12 slim
* Installs `requirements.txt`
* Copies the application code
* Copies Alembic configuration
* Copies `seed.py`
* Copies `run_migrations.py`
* Creates the report directory
* Runs Uvicorn on port 8000

### PostgreSQL Container

`compose.yaml` runs:

```text
postgres:16
```

Database configuration:

```text
Database: tickertrack_dev
User: postgres
```

---

## 20. Docker Architecture

```text
                         Host Machine
                              |
                              |
                       localhost:8000
                              |
                              v
                  +-----------------------+
                  |   TickerTrack API     |
                  |   FastAPI Container   |
                  |   Python 3.12         |
                  |       :8000           |
                  +-----------+-----------+
                              |
                       Docker Network
                              |
                              v
                  +-----------------------+
                  | PostgreSQL Container  |
                  |    PostgreSQL 16      |
                  |   tickertrack_dev     |
                  |       :5432           |
                  +-----------------------+
```

Inside Docker, the API connects to PostgreSQL using:

```text
postgresql+psycopg2://postgres:postgres@db:5432/tickertrack_dev
```

`db` is the PostgreSQL service name defined in `compose.yaml`.

The API does not use `localhost` to reach the database from inside the container.

---

## 21. Docker Healthcheck

PostgreSQL has a healthcheck using:

```text
pg_isready
```

The API waits for PostgreSQL to become healthy before starting.

This ensures the application does not attempt database connections before PostgreSQL is ready.

---

## 22. Docker Volumes

The Docker Compose configuration uses persistent volumes for:

```text
tickertrack-db-data
tickertrack-reports
```

The database volume stores PostgreSQL data.

The reports volume stores generated Excel files.

---

## 23. Docker Setup

Make sure Docker Desktop is running.

Build and start:

```powershell
docker compose up -d --build
```

Check containers:

```powershell
docker compose ps
```

Expected:

```text
tickertrack-db    Up (healthy)
tickertrack-api   Up
```

---

## 24. Run Docker Migrations

The Docker PostgreSQL database is initially empty.

Run:

```powershell
docker compose exec api python run_migrations.py
```

This creates the six application tables.

---

## 25. Seed Docker Database

Run:

```powershell
docker compose exec api python seed.py
```

This loads the provided assessment seed data into the Docker PostgreSQL database.

---

## 26. Access the Dockerized API

Health:

```text
http://localhost:8000/health
```

Swagger:

```text
http://localhost:8000/docs
```

Postman can continue using:

```text
http://127.0.0.1:8000
```

because port 8000 is mapped from the host to the API container.

---

## 27. Docker Logs and Utilities

View API logs:

```powershell
docker compose logs -f api
```

View database logs:

```powershell
docker compose logs -f db
```

Open a shell in the API container:

```powershell
docker compose exec api sh
```

Open PostgreSQL:

```powershell
docker compose exec db psql -U postgres -d tickertrack_dev
```

Check containers:

```powershell
docker compose ps
```

---

## 28. Stop Docker

Stop the application and database containers:

```powershell
docker compose down
```

The Docker volumes remain intact.

Starting again:

```powershell
docker compose up -d
```

will reuse the existing database volume.

---

## 29. Completely Reset Docker

To remove the containers and database/report volumes:

```powershell
docker compose down -v
```

Then rebuild:

```powershell
docker compose up -d --build
```

Run migrations:

```powershell
docker compose exec api python run_migrations.py
```

Seed the database:

```powershell
docker compose exec api python seed.py
```

This creates a completely fresh Docker environment.

---

## 30. Clean Environment Docker Test

The Dockerized application was tested from a clean environment using the following sequence:

```powershell
docker compose down -v
docker compose up -d --build
docker compose exec api python run_migrations.py
docker compose exec api python seed.py
```

The following were then verified:

```text
PostgreSQL container starts
PostgreSQL healthcheck passes
FastAPI container starts
Database migrations succeed
Seed data loads successfully
/health responds successfully
/docs loads successfully
API requests work through Postman
Excel reports can be generated
```

This demonstrates that the project can be reproduced without relying on the host machine's local Python or PostgreSQL installation.

---

## 31. Database Submission Strategy

The PostgreSQL data directory itself is not required to be committed to GitHub.

The database can be reproduced using:

```text
Alembic migrations
+
seed.py
+
Docker PostgreSQL service
```

This allows a fresh environment to reconstruct the complete database schema and initial data.

---

## 32. Clean Clone Setup

### Local

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd scaffold

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

Configure `.env`, create `tickertrack_dev`, then:

```powershell
python run_migrations.py
python seed.py
pytest -q
uvicorn app.main:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

### Docker

With Docker Desktop running:

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd scaffold

docker compose up -d --build
docker compose exec api python run_migrations.py
docker compose exec api python seed.py
```

Open:

```text
http://localhost:8000/docs
```

---

## 33. Known Assumption

The assessment requires report generation to be gated by manager seniority but does not explicitly define the minimum seniority level.

The implementation assumes:

```text
analyst   → cannot generate reports
associate → can generate reports
principal → can generate reports
```

This is documented as an implementation assumption.

---

## 34. Assessment Deliverables

The completed project includes:

* FastAPI backend
* PostgreSQL database
* SQLAlchemy models
* Alembic migrations
* Pydantic schemas
* Portfolio Manager management
* Ticker and price management
* Portfolio holding management
* Manager portfolio isolation
* Aggregate 100% target-weight validation
* Moving-average calculations
* Crossover signal detection
* Signal API
* Excel report generation
* Report download
* Unit tests
* API tests
* Postman testing
* README documentation
* NOTES.md
* Dockerfile
* Docker Compose configuration
* Clean-environment Docker validation

---

## 35. Final Validation

Run the full test suite:

```powershell
pytest -q
```

Expected result:

```text
0 failed
```

Verify Docker:

```powershell
docker compose down -v
docker compose up -d --build
docker compose exec api python run_migrations.py
docker compose exec api python seed.py
```

Then verify:

```text
http://localhost:8000/health
http://localhost:8000/docs
```