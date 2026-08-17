"""
Seed data for TickerTrack — complete and realistic. Do NOT modify this file.

Uses SQLAlchemy Core against the tables created by Alembic migrations, so it
runs correctly before you've written a single line in app/models/.

Run after `alembic upgrade head`:
    python seed.py

Note on AAPL's price series: it is deliberately a 20-day decline (200 -> 181)
so that, once your endpoint is implemented, POSTing one more high price
(as the marker's live test does) mathematically forces a 5-day moving
average to cross above the 20-day moving average — a golden_cross — letting
the automated marker verify FR-4.1 without depending on real market data.
"""
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine, insert

load_dotenv()

engine = create_engine(os.environ["DATABASE_URL"])
metadata = MetaData()
metadata.reflect(bind=engine)

portfolio_managers = metadata.tables["portfolio_managers"]
tickers = metadata.tables["tickers"]
price_snapshots = metadata.tables["price_snapshots"]
portfolio_holdings = metadata.tables["portfolio_holdings"]
reports = metadata.tables["reports"]

TICKER_DEFS = [
    ("AAPL", "Apple Inc.", "Technology"),
    ("MSFT", "Microsoft Corporation", "Technology"),
    ("TSLA", "Tesla Inc.", "Automotive"),
    ("JPM", "JPMorgan Chase & Co.", "Financials"),
    ("NVDA", "NVIDIA Corporation", "Technology"),
]

# AAPL: 20 days, declining 200 -> 181 (step -1) — sets up a clean golden-cross
# test once the marker POSTs a 21st, sharply higher price (see phase4-pipeline.js).
AAPL_SERIES = list(range(200, 180, -1))  # [200, 199, ..., 181] = 20 values

# Other tickers just need enough history for basic report generation —
# 8 days of mild realistic movement, no crossover shape required.
OTHER_SERIES = {
    "MSFT": [410, 412, 408, 415, 413, 417, 420, 418],
    "TSLA": [242, 238, 245, 250, 247, 252, 249, 255],
    "JPM": [195, 196, 194, 197, 198, 196, 199, 200],
    "NVDA": [118, 120, 117, 121, 123, 122, 125, 124],
}

HOLDINGS = {
    "Wong Kah Yan": [("AAPL", 40), ("MSFT", 30), ("NVDA", 20)],   # total 90 — 10% headroom
    "Devan Nathan": [("TSLA", 50), ("JPM", 30)],                    # total 80
    "Farah Idris": [("JPM", 100)],                                   # total 100 — at the cap
}


def main():
    with engine.begin() as conn:
        conn.execute(reports.delete())
        conn.execute(portfolio_holdings.delete())
        conn.execute(price_snapshots.delete())
        conn.execute(tickers.delete())
        conn.execute(portfolio_managers.delete())

        # ── Portfolio managers — covers all 3 seniority levels + 1 inactive ──
        manager_rows = conn.execute(
            insert(portfolio_managers).returning(portfolio_managers.c.id, portfolio_managers.c.name),
            [
                {"name": "Wong Kah Yan", "email": "kah.yan.wong@northgate-am.com", "seniority": "principal", "active": True},
                {"name": "Devan Nathan", "email": "devan.nathan@northgate-am.com", "seniority": "associate", "active": True},
                {"name": "Farah Idris", "email": "farah.idris@northgate-am.com", "seniority": "analyst", "active": True},
                {"name": "Lim Boon Huat", "email": "boon.huat.lim@northgate-am.com", "seniority": "principal", "active": False},
            ],
        ).fetchall()
        manager_ids = {row.name: row.id for row in manager_rows}

        # ── Tickers (reference table) ────────────────────────────────────────
        ticker_rows = conn.execute(
            insert(tickers).returning(tickers.c.id, tickers.c.symbol),
            [{"symbol": s, "company_name": n, "sector": sec, "is_active": True} for (s, n, sec) in TICKER_DEFS],
        ).fetchall()
        ticker_ids = {row.symbol: row.id for row in ticker_rows}

        # ── Price snapshots ───────────────────────────────────────────────────
        start_date = datetime.utcnow() - timedelta(days=20)

        for day_offset, price in enumerate(AAPL_SERIES):
            conn.execute(
                insert(price_snapshots),
                [{
                    "ticker_id": ticker_ids["AAPL"],
                    "price": price,
                    "volume": 55_000_000 + day_offset * 120_000,
                    "captured_at": start_date + timedelta(days=day_offset),
                    "source": "seed",
                }],
            )

        other_start = datetime.utcnow() - timedelta(days=8)
        for symbol, prices in OTHER_SERIES.items():
            for day_offset, price in enumerate(prices):
                conn.execute(
                    insert(price_snapshots),
                    [{
                        "ticker_id": ticker_ids[symbol],
                        "price": price,
                        "volume": 20_000_000 + day_offset * 90_000,
                        "captured_at": other_start + timedelta(days=day_offset),
                        "source": "seed",
                    }],
                )

        # ── Portfolio holdings — supports isolation + 100%-total tests ───────
        for manager_name, holdings in HOLDINGS.items():
            conn.execute(
                insert(portfolio_holdings),
                [
                    {
                        "manager_id": manager_ids[manager_name],
                        "ticker_id": ticker_ids[symbol],
                        "target_weight_pct": weight,
                        "added_at": datetime.utcnow(),
                    }
                    for (symbol, weight) in holdings
                ],
            )

        # ── One sample report row (metadata only) ─────────────────────────────
        conn.execute(
            insert(reports),
            [{
                "manager_id": manager_ids["Wong Kah Yan"],
                "date_from": start_date.date(),
                "date_to": (start_date + timedelta(days=19)).date(),
                "filename": "tickertrack_report_sample.xlsx",
                "row_count": 20,
                "generated_at": datetime.utcnow(),
            }],
        )

    total_snapshots = len(AAPL_SERIES) + sum(len(v) for v in OTHER_SERIES.values())
    total_holdings = sum(len(v) for v in HOLDINGS.values())
    print(f"Seeded {len(manager_ids)} managers, {len(ticker_ids)} tickers, "
          f"{total_snapshots} price snapshots, {total_holdings} holdings, 1 report.")


if __name__ == "__main__":
    main()
