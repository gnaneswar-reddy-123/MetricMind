from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine

router = APIRouter(prefix="/api/trends", tags=["Trends"])


@router.get("/revenue")
def revenue_trend():
    sql = """
        SELECT
            YEAR(order_date) AS year,
            QUARTER(order_date) AS quarter,
            ROUND(SUM(revenue), 2) AS revenue
        FROM sales
        GROUP BY YEAR(order_date), QUARTER(order_date)
        ORDER BY YEAR(order_date), QUARTER(order_date)
    """

    with engine.connect() as connection:
        results = connection.execute(text(sql)).mappings().all()

    return {
        "chart_type": "line",
        "title": "Revenue Trend Over Time",
        "data": [
            {
                "period": f"Q{row['quarter']} {row['year']}",
                "revenue": float(row["revenue"])
            }
            for row in results
        ]
    }