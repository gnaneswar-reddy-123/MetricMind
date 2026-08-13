from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine

router = APIRouter(prefix="/api/charts", tags=["Charts"])


@router.get("/revenue-by-region")
def revenue_by_region():
    sql = """
        SELECT
            region,
            ROUND(SUM(revenue), 2) AS revenue
        FROM sales
        GROUP BY region
        ORDER BY revenue DESC
    """

    with engine.connect() as connection:
        results = connection.execute(text(sql)).mappings().all()

    return {
        "chart_type": "bar",
        "title": "Revenue by Region",
        "data": [
            {
                "region": row["region"],
                "revenue": float(row["revenue"])
            }
            for row in results
        ]
    }