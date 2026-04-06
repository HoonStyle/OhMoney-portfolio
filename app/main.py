"""
FastAPI Application — Entry point for the OhMoney backend.

Mounts:
    - REST API routers (agents, analytics, scheduler, videos, etc.)
    - Prometheus metrics instrumentation
    - Vue 3 SPA at /frontend/
    - Health check endpoint
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="OhMoney Orchestrator", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:9100",  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

# --- Router registration ---
# app.include_router(agents_router, prefix="/agents", tags=["agents"])
# app.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
# app.include_router(scheduler_router, prefix="/scheduler", tags=["scheduler"])
# app.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
# app.include_router(videos_router, prefix="/videos", tags=["videos"])
# app.include_router(shop_router, prefix="/shop", tags=["shop"])
# app.include_router(telegram_router, prefix="/telegram", tags=["telegram"])


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    """Wait for DB tables, initialize metrics, start background tasks."""
    ...


@app.on_event("shutdown")
async def shutdown_event():
    """Gracefully stop scheduler and close ARQ pool."""
    ...
