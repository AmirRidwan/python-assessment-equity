from datetime import datetime

from fastapi import FastAPI

from app.error_handlers import register_error_handlers
from app.routers import managers, tickers, holdings, signals, reports

app = FastAPI(title="TickerTrack Portfolio Monitor API")

register_error_handlers(app)

app.include_router(managers.router, prefix="/managers", tags=["managers"])
app.include_router(tickers.router, prefix="/tickers", tags=["tickers"])
app.include_router(holdings.router, prefix="/holdings", tags=["holdings"])
app.include_router(signals.router, prefix="/signals", tags=["signals"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
