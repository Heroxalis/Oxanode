from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.api.auth import require_admin

router = APIRouter(
    prefix="/api/metrics",
    tags=["Metrics"],
)

@router.get("/latest")
async def get_latest_metrics(
    request: Request,
    _: bool = Depends(require_admin),
):
    metrics_service = getattr(
        request.app.state,
        "metrics_service",
        None,
    )

    if metrics_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Metrics service is unavailable.",
        )

    snapshot = metrics_service.get_latest_snapshot()

    if snapshot is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Metrics snapshot is not available yet.",
        )

    return snapshot
