from fastapi import APIRouter, Query
from app.services.root_cause_service import analyze_root_cause

router = APIRouter(
    prefix="/api/root-cause",
    tags=["Root Cause Analysis"]
)


@router.get("/analyze")
def analyze(
    region: str = Query(...),
    year: int | None = None,
    quarter: int | None = Query(None, ge=1, le=4)
):
    return analyze_root_cause(
        region=region,
        year=year,
        quarter=quarter
    )