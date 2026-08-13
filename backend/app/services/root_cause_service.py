from sqlalchemy import text
from app.database import engine


def analyze_root_cause(region: str, year: int = None, quarter: int = None):

    sql = """
        SELECT
            SUM(revenue) AS total_revenue,
            SUM(cost) AS total_cost,
            SUM(shipping_cost) AS total_shipping_cost,
            SUM(material_cost) AS total_material_cost,
            SUM(revenue) - SUM(cost) AS profit,

            CASE
                WHEN SUM(revenue) = 0 THEN 0
                ELSE (
                    (SUM(revenue) - SUM(cost))
                    / SUM(revenue)
                ) * 100
            END AS margin_percentage

        FROM sales
        WHERE region = :region
    """

    params = {
        "region": region
    }

    if year is not None:
        sql += " AND YEAR(order_date) = :year"
        params["year"] = year

    if quarter is not None:
        sql += " AND QUARTER(order_date) = :quarter"
        params["quarter"] = quarter

    with engine.connect() as connection:
        result = connection.execute(
            text(sql),
            params
        ).mappings().first()

    if result["total_revenue"] is None:
        return {
            "error": "No data found",
            "region": region,
            "year": year,
            "quarter": quarter
        }

    revenue = float(result["total_revenue"] or 0)
    cost = float(result["total_cost"] or 0)
    shipping_cost = float(result["total_shipping_cost"] or 0)
    material_cost = float(result["total_material_cost"] or 0)
    profit = float(result["profit"] or 0)
    margin = float(result["margin_percentage"] or 0)

    # Calculate cost percentages
    shipping_percentage = (
        (shipping_cost / revenue) * 100
        if revenue > 0 else 0
    )

    material_percentage = (
        (material_cost / revenue) * 100
        if revenue > 0 else 0
    )

    # Determine primary cause
    if shipping_cost > material_cost:
        primary_cause = "shipping_cost"
        explanation = (
            "Shipping cost is the largest identified cost component "
            "and is significantly affecting profitability."
        )
    else:
        primary_cause = "material_cost"
        explanation = (
            "Material cost is the largest identified cost component "
            "and is significantly affecting profitability."
        )

    # Determine severity
    if margin < 40:
        severity = "critical"
        conclusion = (
            f"Critical margin decline detected. Margin is only "
            f"{round(margin, 2)}%. "
            f"High {primary_cause} is a major contributor."
        )
    elif margin < 50:
        severity = "warning"
        conclusion = (
            f"Margin is below the expected level at "
            f"{round(margin, 2)}%. "
            f"The main contributor is {primary_cause}."
        )
    else:
        severity = "healthy"
        conclusion = (
            f"Margin is healthy at {round(margin, 2)}%. "
            f"No critical margin issue was detected."
        )

    return {
        "region": region,
        "year": year,
        "quarter": quarter,

        "analysis": {
            "total_revenue": round(revenue, 2),
            "total_cost": round(cost, 2),
            "shipping_cost": round(shipping_cost, 2),
            "material_cost": round(material_cost, 2),
            "profit": round(profit, 2),
            "margin_percentage": round(margin, 2),

            "shipping_cost_percentage_of_revenue":
                round(shipping_percentage, 2),

            "material_cost_percentage_of_revenue":
                round(material_percentage, 2)
        },

        "root_cause": {
            "severity": severity,
            "primary_cause": primary_cause,
            "explanation": explanation
        },

        "conclusion": conclusion
    }