# TickerTrack Assessment Notes

## 1. Overview

This assessment was completed as a practical evaluation of the Python backend training covering FastAPI, SQLAlchemy, Alembic, PostgreSQL, Pydantic, testing and Excel reporting.

The main objective was to complete the supplied TickerTrack scaffold without rebuilding the provided infrastructure and to implement the application logic defined in the assessment brief.

---

## 2. What Was Most Challenging

### 2.1 PostgreSQL ENUM Migration Issue

One of the earliest challenges was getting the supplied Alembic migrations running.

The provided migration creates PostgreSQL ENUM types explicitly before creating tables that contain those ENUM columns. With the pinned SQLAlchemy version, the table creation process also attempted to create the ENUM, resulting in a duplicate PostgreSQL type error.

The development environment also encountered a PostgreSQL schema issue where the `public` schema was not available as the active schema.

The final approach kept the provided migration files unchanged and used a separate migration runner as a local compatibility workaround.

---

### 2.2 SQLAlchemy Model Mapping

The supplied model files initially contained TODO placeholders.

The models had to be implemented to match the existing database schema exactly, including:

* Primary keys
* Foreign keys
* PostgreSQL ENUMs
* Unique constraints
* Numeric precision
* Relationships
* Server-side timestamp defaults

A primary-key mapping issue initially caused SQLAlchemy to report that it could not assemble the primary key for `portfolio_managers`.

The issue was resolved by implementing all model definitions correctly.

---

### 2.3 Decimal vs Float Handling

A runtime error occurred while processing price snapshots:

```text
TypeError: unsupported operand type(s) for +:
'decimal.Decimal' and 'float'
```

The problem occurred because PostgreSQL `NUMERIC` values were returned as `Decimal`, while the API schema initially represented price values as `float`.

The solution was to use `Decimal` consistently for financial values, including:

* Price
* Target portfolio weight
* 5-day moving average
* 20-day moving average

This avoids mixing floating-point and decimal arithmetic.

---

### 2.4 Manager Portfolio Isolation

One of the key business requirements was ensuring that a manager can only access their own holdings.

The application uses the existing `X-Manager-Id` dependency and filters portfolio holdings by the resolved manager ID.

This was also covered by API tests for Manager A and Manager B to ensure that one manager's holdings are not exposed to another manager.

---

### 2.5 Aggregate Portfolio Weight Constraint

The 100% portfolio rule required more than a simple database uniqueness constraint.

For a new holding, the complete portfolio total must remain:

```text
existing total + new weight <= 100%
```

For an update:

```text
current total - old weight + new weight <= 100%
```

This logic was extracted into pure business-logic functions so that it could be independently unit tested.

---

### 2.6 Moving Average Crossover Detection

The crossover requirement required comparing both the previous and current moving-average states.

A golden cross is not simply:

```text
5MA > 20MA
```

It requires an actual transition:

```text
previous 5MA <= previous 20MA
current 5MA > current 20MA
```

Similarly, a death cross requires the opposite transition.

The logic was separated into a pure function so it could be tested independently from FastAPI and SQLAlchemy.

---

### 2.7 Excel Report Generation

The reporting stage required combining several sources of information:

* Raw prices
* 5-day moving averages
* 20-day moving averages
* Percentage change
* Portfolio target weights
* Crossover signals

The report was generated using `openpyxl`.

Additional formatting was added for readability, including highlighted crossover rows, column sizing and frozen headers.

---

## 3. Key Design Decisions

### 3.1 Keep the Supplied Database Infrastructure

The provided:

```text
alembic/versions/*.py
app/database.py
app/dependencies.py
app/error_handlers.py
app/main.py
seed.py
```

were treated as assessment infrastructure.

Application logic was implemented around the provided structure rather than replacing it.

---

### 3.2 Separate Business Logic From Routes

Pure calculations were moved into:

```text
app/business_logic/
├── moving_average.py
├── crossover.py
└── portfolio.py
```

This keeps the route handlers focused on API and database responsibilities while allowing core business rules to be unit tested independently.

---

### 3.3 Use PostgreSQL NUMERIC With Decimal

Financial calculations use `Decimal` to match PostgreSQL `NUMERIC` fields.

This avoids unnecessary floating-point precision issues and prevents type mismatches between the database and Python calculation layer.

---

### 3.4 Use X-Manager-Id for Portfolio Scoping

The existing scaffold dependency resolves the manager from:

```http
X-Manager-Id
```

The resulting manager is used to scope operations on:

```text
portfolio_holdings
reports
```

This prevents clients from directly selecting another manager's portfolio.

---

### 3.5 Keep Server-Computed Signal Types

Clients do not send:

```text
golden_cross
death_cross
```

when recording a price.

The server calculates moving averages and determines the crossover signal from the actual data.

This prevents clients from creating false signal types.

---

## 4. Testing Approach

The testing strategy has two layers.

### Unit Tests

Pure business logic was tested without depending on the API:

```text
test_moving_average.py
test_crossover.py
test_portfolio.py
```

These verify:

* Correct rolling averages
* Golden cross detection
* Death cross detection
* No crossover
* Missing MA handling
* Portfolio total at less than 100%
* Portfolio total exactly at 100%
* Portfolio total above 100%
* Correct update calculations

### API Tests

FastAPI `TestClient` was used to test actual endpoints:

```text
test_managers.py
test_prices.py
test_holdings.py
test_signals.py
test_reports.py
```

The API tests cover the assessment's important functional and business rules.

---

## 5. Manual Testing

Postman was used for manual API verification.

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
ticker_id
report_id
```

The `X-Manager-Id` header was added to manager-scoped requests.

---

## 6. Known Limitations

### 6.1 External Market Data Provider

The core assessment implementation supports recording price snapshots through the API.

A production-ready version could integrate a dedicated market-data API to automatically fetch prices.

The external data source should be isolated behind a service layer so network failures can be converted into clean 502/503 responses.

---

### 6.2 Report Seniority Rule

The assessment requires report generation to be gated by manager seniority but does not explicitly define the required threshold.

The implementation assumes:

```text
analyst   → rejected
associate → allowed
principal → allowed
```

This is an implementation assumption and should be confirmed with the assessment owner if a different policy is expected.

---

### 6.3 Test Database Isolation

The API tests currently run against the development/test database and create test records.

For a production-grade CI/CD setup, a separate test database with transaction rollback or disposable database fixtures would be preferable.

---

### 6.4 Authentication

The assessment explicitly does not require full authentication.

The `X-Manager-Id` header is therefore only a simulation of the active manager and should not be treated as a secure authentication mechanism in production.

---

## 7. Improvements for a Production Version

Possible future improvements include:

* Real authentication and authorization
* Dedicated test database
* Service/repository layer for database access
* Market-data provider integration
* Background jobs for price ingestion
* More comprehensive report formatting
* Structured logging
* API versioning
* Rate limiting
* Centralized configuration using Pydantic Settings
* CI/CD pipeline
* Code coverage reporting
* More comprehensive integration tests
* Better report storage management

---

## 8. Final Reflection

The most valuable part of the assessment was integrating several technologies into one complete backend workflow rather than working with isolated examples.

The project required connecting:

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
openpyxl Excel Reporting
```

The assessment also reinforced the importance of separating:

```text
API concerns
Business rules
Database models
Testing
Reporting
```

The most useful lesson was that working functionality is not enough on its own. Business rules such as portfolio isolation, aggregate target weights and server-computed crossover signals need to be explicitly validated through automated tests.

---

## 9. Final Assessment Status

The implemented project covers the main assessment requirements:

* Portfolio Manager management
* Ticker reference data
* Price snapshot management
* Portfolio holding management
* Manager portfolio isolation
* 100% portfolio target-weight constraint
* Moving-average calculation
* Golden/death crossover detection
* Signal listing and filtering
* Excel report generation
* Report download
* Unit tests
* API tests
* PostgreSQL persistence
* Alembic migration support
* Pydantic validation

The final validation command is:

```powershell
pytest -q
```

A successful assessment run should finish with:

```text
0 failed
```
