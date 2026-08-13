from fastapi import APIRouter, Query
from app.services.semantic_service import (
    get_available_metrics,
    get_metric_summary
)

router = APIRouter(
    prefix="/api/metrics",
    tags=["Metrics"]
)


@router.get("/")
def metrics():
    return get_available_metrics()


@router.get("/summary")
def metric_summary(
    metric: str = Query(...),
    region: str | None = None
):
    return get_metric_summary(metric, region)