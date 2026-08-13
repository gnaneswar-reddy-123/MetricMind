from fastapi import APIRouter, Query
from app.services.recommendation_service import generate_recommendation

router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"]
)


@router.get("/generate")
def generate(
    region: str = Query(...),
    year: int | None = None,
    quarter: int | None = Query(None, ge=1, le=4)
):
    return generate_recommendation(
        region=region,
        year=year,
        quarter=quarter
    )