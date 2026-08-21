# TickerTrack Assessment Notes

## 1. Overview

This assessment was completed as a practical evaluation of the Python backend training covering FastAPI, SQLAlchemy, Alembic, PostgreSQL, Pydantic, testing, API development and Excel reporting.

The main objective was to complete the supplied TickerTrack scaffold without rebuilding the provided infrastructure and to implement the application logic defined in the assessment brief. The completed project includes Portfolio Manager management, ticker and price snapshot handling, manager-scoped portfolio holdings, aggregate portfolio-weight validation, moving-average crossover detection, Excel report generation, automated testing and Postman validation. As a bonus, the completed application and PostgreSQL database were also containerized using Docker and Docker Compose and tested from a clean environment.

---

## 2. What Was Most Challenging

### 2.1 PostgreSQL ENUM Migration Issue

One of the earliest challenges was getting the supplied Alembic migrations running.

The provided migration creates PostgreSQL ENUM types explicitly before creating tables that contain those ENUM columns. With the pinned SQLAlchemy version, the table creation process also attempted to create the ENUM, resulting in a duplicate PostgreSQL type error.

The development environment also encountered a PostgreSQL schema issue where the `public` schema was not available as the active schema.

The assessment explicitly required the supplied migration files to remain unchanged. The final approach therefore kept `alembic/versions/*.py` untouched and used a separate `run_migrations.py` compatibility runner to execute the provided migrations successfully.

This provided practical experience with:

* PostgreSQL ENUM types
* SQLAlchemy PostgreSQL behavior
* Alembic migration execution
* PostgreSQL schemas and search paths
* Database state management

---

### 2.2 SQLAlchemy Model Mapping

The supplied model files initially contained TODO placeholders.

The following models had to be implemented to match the existing database schema:

* `PortfolioManager`
* `Ticker`
* `PriceSnapshot`
* `PortfolioHolding`
* `CrossoverSignal`
* `Report`

The implementation included:

* Primary keys
* Foreign keys
* Unique constraints
* PostgreSQL ENUMs
* Numeric precision
* Relationships
* Server-side timestamp defaults
* Boolean defaults

An initial mapper error occurred because `PortfolioManager` did not have a primary key defined.

The issue was resolved by completing the SQLAlchemy model definitions and ensuring they matched the provided schema and migration structure.

---

### 2.3 Decimal vs Float Handling

A runtime error occurred while processing price snapshots:

```text
TypeError: unsupported operand type(s) for +:
'decimal.Decimal' and 'float'
```

The problem occurred because PostgreSQL `NUMERIC` values were returned as `Decimal`, while the API schema initially represented price values as `float`.

The final implementation uses `Decimal` consistently for financial values, including:

* Price
* Target portfolio weight
* 5-day moving average
* 20-day moving average

This keeps the database, API schema and business-logic calculations consistent and avoids mixing floating-point and decimal arithmetic.

---

### 2.4 Manager Portfolio Isolation

One of the key business requirements was ensuring that a manager can only access their own holdings.

The existing `X-Manager-Id` dependency is used to resolve the current manager, and all holding queries are scoped using that manager ID.

For example:

```text
Manager A
    ↓
GET /holdings/
    ↓
Only Manager A's holdings
```

Manager A cannot access Manager B's holdings.

This was explicitly validated through API tests using two separate managers and different ticker holdings.

---

### 2.5 Aggregate Portfolio Weight Constraint

The 100% portfolio-weight requirement required more than a normal unique database constraint.

For a new holding, the complete portfolio must remain:

```text
existing total + new weight <= 100%
```

For an update:

```text
current total - old weight + new weight <= 100%
```

The validation logic was extracted into pure business-logic functions so it could be independently tested.

The implementation also allows exactly 100% while rejecting any total above 100%.

---

### 2.6 Moving Average Crossover Detection

The crossover requirement required comparing both the previous and current moving-average states.

A golden cross is detected when:

```text
Previous:
5MA <= 20MA

Current:
5MA > 20MA
```

A death cross is detected when:

```text
Previous:
5MA >= 20MA

Current:
5MA < 20MA
```

The implementation does not simply check whether the 5-day average is currently above or below the 20-day average.

The crossover logic was separated into a pure function so it could be independently unit tested.

---

### 2.7 Excel Report Generation

The reporting stage required combining several sources of information:

* Raw prices
* 5-day moving averages
* 20-day moving averages
* Percentage changes
* Portfolio target weights
* Crossover signals

The report was generated using `openpyxl`.

Additional formatting was implemented for readability, including:

* Highlighted crossover rows
* Frozen header rows
* Column sizing
* Number formatting
* Notes for insufficient price history

Tickers with fewer than 20 snapshots in the reporting range are still included with their raw prices instead of being excluded.

---

### 2.8 Automated Testing

A complete automated testing structure was added under `tests/`.

The project includes:

```text
tests/
├── unit/
│   ├── test_moving_average.py
│   ├── test_crossover.py
│   └── test_portfolio.py
│
└── api/
    ├── conftest.py
    ├── test_managers.py
    ├── test_prices.py
    ├── test_holdings.py
    ├── test_signals.py
    └── test_reports.py
```

The tests cover both pure business logic and complete API behavior.

The final test suite was executed successfully with all tests passing.

---

## 3. Key Design Decisions

### 3.1 Keep the Supplied Infrastructure

The following provided components were treated as protected assessment infrastructure:

```text
alembic/versions/*.py
app/database.py
app/dependencies.py
app/error_handlers.py
app/main.py
seed.py
```

The application was implemented around the existing scaffold instead of replacing or redesigning the provided infrastructure.

---

### 3.2 Separate Business Logic From Routes

Pure business calculations were moved into:

```text
app/business_logic/
├── moving_average.py
├── crossover.py
└── portfolio.py
```

This keeps route handlers focused on API and database responsibilities while making the core business rules easier to understand, reuse and test.

---

### 3.3 Use Decimal for Financial Values

`Decimal` is used for financial data because the PostgreSQL schema uses `NUMERIC` columns.

This avoids unnecessary floating-point precision problems and prevents type conflicts between database values and Python calculations.

---

### 3.4 Use X-Manager-Id for Portfolio Scoping

The existing dependency resolves the manager from:

```http
X-Manager-Id
```

The resulting manager is then used to scope:

```text
portfolio_holdings
reports
```

This prevents clients from directly selecting another manager's portfolio by supplying a different `manager_id` in the request body.

---

### 3.5 Keep Signal Types Server-Computed

Clients do not submit:

```text
golden_cross
death_cross
```

when recording a price.

The server calculates the moving averages and determines the signal from the actual price history.

This prevents clients from creating false crossover signals.

---

### 3.6 Use Postman for Manual API Validation

Postman was used alongside automated tests to manually verify the API workflow.

The collection was organized into:

```text
Health
Managers
Tickers
Holdings
Signals
Reports
```

Environment variables were used for:

```text
base_url
manager_id
manager_a_id
manager_b_id
ticker_id
aapl_ticker_id
report_id
```

This made it easier to test manager isolation, portfolio constraints, price ingestion and report generation.

---

## 4. Testing Approach

The testing strategy has two layers.

### Unit Tests

Pure business logic was tested without requiring the API:

```text
test_moving_average.py
test_crossover.py
test_portfolio.py
```

These tests verify:

* Correct rolling averages
* Insufficient moving-average data
* Golden-cross detection
* Death-cross detection
* No-crossover scenarios
* Missing MA values
* Portfolio totals below 100%
* Portfolio totals exactly at 100%
* Portfolio totals above 100%
* Correct update-weight calculations

---

### API Tests

FastAPI `TestClient` was used to test actual HTTP endpoints:

```text
test_managers.py
test_prices.py
test_holdings.py
test_signals.py
test_reports.py
```

The API tests cover the main assessment requirements, including:

#### Managers

* Manager creation
* Email validation
* Duplicate email prevention
* Manager retrieval
* Manager updates
* Manager deactivation
* Unsupported manager deletion
* Pagination

#### Prices

* Ticker listing
* AAPL lookup
* Price history
* Price pagination
* Valid price creation
* Negative price rejection
* Zero price rejection
* Negative volume rejection
* Unknown ticker handling
* Out-of-order snapshot rejection
* Equal timestamp rejection

#### Holdings

* Missing `X-Manager-Id`
* Manager-specific portfolio access
* Manager A / Manager B isolation
* Duplicate holdings
* 100% aggregate constraint
* Exact 100% portfolio
* Holding updates
* Update weight constraint
* Missing holdings
* Holding deletion
* Inactive manager handling

#### Signals

* Signal listing
* Ticker filtering
* Pagination
* Unknown ticker handling

#### Reports

* Missing manager header
* Empty portfolio handling
* Invalid date ranges
* Report generation
* Report listing
* Report isolation
* Report download
* Missing report-file handling
* Inactive manager handling

The complete automated test suite passed successfully.

---

## 5. Manual Testing

Postman was used to complement the automated API tests.

The following workflows were manually verified:

```text
Manager creation
Manager update/deactivation
Duplicate email
Ticker listing
Price creation
Price validation
Out-of-order price rejection
Portfolio isolation
100% portfolio constraint
Holding update/delete
Signal listing/filtering
Excel report generation
Report download
```

The `X-Manager-Id` header was added to all manager-scoped requests.

---

## 6. Docker Bonus Implementation

As the bonus task, the completed FastAPI application and PostgreSQL database were containerized using Docker and Docker Compose.

The Docker architecture consists of two services:

```text
FastAPI Application Container
            |
       Docker Network
            |
PostgreSQL Database Container
```

---

### 6.1 FastAPI Container

The `Dockerfile` uses:

```text
python:3.12-slim
```

The image:

1. Sets `/app` as the working directory
2. Installs all dependencies from `requirements.txt`
3. Copies the application source
4. Copies Alembic configuration
5. Copies `seed.py`
6. Copies `run_migrations.py`
7. Creates the report directory
8. Starts Uvicorn on port 8000

---

### 6.2 PostgreSQL Container

The Docker Compose database service uses:

```text
postgres:16
```

with:

```text
Database: tickertrack_dev
User: postgres
```

Inside Docker, the API connects to the PostgreSQL service using:

```text
db
```

rather than `localhost`.

The Docker database connection is:

```text
postgresql+psycopg2://postgres:postgres@db:5432/tickertrack_dev
```

---

### 6.3 Database Healthcheck

PostgreSQL uses a `pg_isready` healthcheck.

The API waits for the database to become healthy before starting.

The expected flow is:

```text
Start PostgreSQL
      ↓
PostgreSQL healthcheck
      ↓
Database ready
      ↓
Start FastAPI
```

---

### 6.4 Docker Volumes

Two Docker-managed volumes are used:

```text
tickertrack-db-data
tickertrack-reports
```

The database volume preserves PostgreSQL data.

The report volume preserves generated Excel files.

---

### 6.5 Docker Clean-Environment Test

The Docker application was tested from a clean environment using:

```powershell
docker compose down -v
docker compose up -d --build
docker compose exec api python run_migrations.py
docker compose exec api python seed.py
```

After rebuilding from scratch, the following were verified:

```text
PostgreSQL container starts successfully
PostgreSQL healthcheck passes
FastAPI container starts successfully
Alembic migrations complete successfully
Seed data loads successfully
/health responds successfully
/docs loads successfully
Postman can communicate with the containerized API
Portfolio APIs work
Signal APIs work
Excel reports can be generated
```

This demonstrates that the project can be reproduced in a new environment without relying on the host machine's local Python installation or PostgreSQL database.

---

## 7. Docker Commands

### Build and Start

```powershell
docker compose up -d --build
```

### Check Services

```powershell
docker compose ps
```

### Run Migrations

```powershell
docker compose exec api python run_migrations.py
```

### Seed Database

```powershell
docker compose exec api python seed.py
```

### View API Logs

```powershell
docker compose logs -f api
```

### View Database Logs

```powershell
docker compose logs -f db
```

### Open API Container Shell

```powershell
docker compose exec api sh
```

### Open PostgreSQL

```powershell
docker compose exec db psql -U postgres -d tickertrack_dev
```

### Stop Containers

```powershell
docker compose down
```

### Completely Reset Docker

```powershell
docker compose down -v
```

---

## 8. Known Limitations

### 8.1 External Market Data Provider

The core assessment implementation focuses on receiving and processing price snapshots through the API.

A production implementation could integrate a dedicated market-data provider for automated price ingestion.

The external service should be isolated behind a service layer, with network failures translated into clean 502/503 responses.

---

### 8.2 Report Seniority Rule

The assessment requires report generation to be gated by manager seniority but does not explicitly define the minimum required level.

The implementation assumes:

```text
analyst   → rejected
associate → allowed
principal → allowed
```

This is an implementation assumption and should be confirmed with the assessment owner if the actual business policy differs.

---

### 8.3 Test Database Isolation

The API tests currently operate against the available application database and create test records.

For a production-grade CI/CD environment, a dedicated PostgreSQL test database or disposable test container would be preferable.

Potential improvements include:

* Transaction rollback fixtures
* Test database containers
* Factory-based test data
* Isolated integration test environments

---

### 8.4 Authentication

The assessment does not require full authentication.

The `X-Manager-Id` header is therefore only an authentication/manager simulation and should not be considered a secure authentication mechanism in a production environment.

---

## 9. Improvements for a Production Version

Potential future improvements include:

* Real authentication and authorization
* Dedicated test database
* Service/repository layer
* External market-data integration
* Background jobs for price ingestion
* More advanced Excel formatting
* Structured logging
* API versioning
* Rate limiting
* Centralized configuration
* CI/CD automation
* Code coverage reporting
* More comprehensive integration tests
* Better report file storage management
* Cloud/object storage for generated reports

---

## 10. Final Reflection

The most valuable part of the assessment was integrating several technologies into one complete backend workflow rather than working with isolated examples.

The final application connects:

```text
FastAPI
    ↓
Pydantic
    ↓
SQLAlchemy
    ↓
PostgreSQL
    ↓
Business Logic
    ↓
Automated Tests
    ↓
Excel Reporting
    ↓
Docker
```

The assessment reinforced the importance of separating:

```text
API concerns
Business rules
Database models
Testing
Reporting
Deployment
```

A particularly useful lesson was that implementing functionality is only one part of completing a backend application. Business rules such as portfolio isolation, aggregate target weights and server-computed crossover signals need to be explicitly tested to ensure the implementation behaves correctly.

The troubleshooting process also improved my understanding of database migration behavior, PostgreSQL ENUM types, schema configuration, data types and containerized service communication.

Docker was an additional opportunity to understand how a Python application and database can be packaged as independent services and reproduced in a clean environment.

---

## 11. Final Assessment Status

The completed project covers the main assessment requirements:

```text
✅ Project structure and configuration
✅ PostgreSQL database
✅ SQLAlchemy models
✅ Alembic migrations
✅ Pydantic schemas
✅ Portfolio Manager management
✅ Ticker reference data
✅ Price snapshot management
✅ Price validation
✅ Portfolio holding management
✅ Manager portfolio isolation
✅ 100% aggregate target-weight constraint
✅ Holding update constraint
✅ Moving-average calculation
✅ Golden-cross detection
✅ Death-cross detection
✅ Server-computed crossover signals
✅ Signal listing/filtering
✅ Excel report generation
✅ Report download
✅ Missing report-file handling
✅ Pagination
✅ Unit tests
✅ API tests
✅ Postman validation
✅ Dockerized application
✅ Dockerized PostgreSQL
✅ Clean-environment Docker testing
✅ Project documentation
```

Final automated validation:

```powershell
pytest -q
```

The final test suite completed successfully with:

```text
0 failed
```
