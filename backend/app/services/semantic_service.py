from sqlalchemy import text
from app.database import engine


METRICS = {
    "revenue": {
        "label": "Revenue",
        "description": "Total sales revenue",
        "sql": "SUM(revenue)"
    },
    "cost": {
        "label": "Cost",
        "description": "Total business cost",
        "sql": "SUM(cost)"
    },
    "profit": {
        "label": "Profit",
        "description": "Revenue minus Cost",
        "sql": "SUM(revenue) - SUM(cost)"
    },
    "margin": {
        "label": "Margin Percentage",
        "description": "Profit divided by Revenue multiplied by 100",
        "sql": """
            CASE
                WHEN SUM(revenue) = 0 THEN 0
                ELSE ((SUM(revenue) - SUM(cost)) / SUM(revenue)) * 100
            END
        """
    }
}
REGION_MAPPING = {
    "asia": "Asia Pacific",
    "asia pacific": "Asia Pacific",
    "europe": "Europe",
    "south america": "South America",
    "north america": "North America"
}

MAX_QUERY_ROWS = 10000


def get_available_metrics():
    return {
        key: {
            "label": value["label"],
            "description": value["description"]
        }
        for key, value in METRICS.items()
    }


def get_metric_summary(metric: str, region: str = None):
    metric = metric.lower()

    if region:
        region = REGION_MAPPING.get(region.lower(), region)

    if metric not in METRICS:
        return {
            "error": f"Metric '{metric}' is not allowed",
            "available_metrics": list(METRICS.keys())
        }
    query_check = check_query_limit(region)

    if not query_check["allowed"]:
        return {
            "error": "Query exceeds the configured row limit",
            "cost_governance": query_check
        }
    

    metric_sql = METRICS[metric]["sql"]

    sql = f"""
        SELECT
            {metric_sql} AS value
        FROM sales
    """

    params = {}

    if region:
        sql += " WHERE region = :region"
        params["region"] = region

    with engine.connect() as connection:
        result = connection.execute(
            text(sql),
            params
        ).mappings().first()

    return {
        "metric": metric,
        "label": METRICS[metric]["label"],
        "value": round(float(result["value"] or 0), 2),
        "region": region,
        "generated_sql": sql.strip()
    }
def check_query_limit(region: str = None):
    sql = "SELECT COUNT(*) AS total_rows FROM sales"
    params = {}

    if region:
        sql += " WHERE region = :region"
        params["region"] = region

    with engine.connect() as connection:
        result = connection.execute(
            text(sql),
            params
        ).mappings().first()

    total_rows = result["total_rows"]

    return {
        "allowed": total_rows <= MAX_QUERY_ROWS,
        "rows_scanned": total_rows,
        "max_rows_allowed": MAX_QUERY_ROWS
    }