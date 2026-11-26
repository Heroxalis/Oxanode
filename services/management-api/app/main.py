from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.metrics import router as metrics_router
from app.core.installation import load_installation
from app.services.authentication import AuthenticationService
from app.services.metrics import MetricsService
from app.services.rate_limiter import LoginRateLimiter

@asynccontextmanager
async def lifespan(app: FastAPI):
    config = load_installation()

    if config is not None:
        app.state.config = config
        app.state.auth_service = AuthenticationService(config)
        app.state.rate_limiter = LoginRateLimiter(config)

        metrics_service = MetricsService(interval=2.0)
        app.state.metrics_service = metrics_service

        await metrics_service.start()
    else:
        app.state.config = None
        app.state.auth_service = None
        app.state.rate_limiter = None
        app.state.metrics_service = None

    try:
        yield
    finally:
        metrics_service = getattr(
            app.state,
            "metrics_service",
            None,
        )

        if metrics_service is not None:
            await metrics_service.stop()

app = FastAPI(
    title="Oxanode Management API",
    description="Backend management service for Oxanode.",
    version="0.1.0-dev",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(metrics_router)

@app.get("/api/health")
async def health_check():
    return {
        "status": "online",
        "service": "oxanode-management-api",
        "version": "0.1.0-dev",
    }
