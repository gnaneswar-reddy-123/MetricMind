from app.services.root_cause_service import analyze_root_cause


def generate_recommendation(region: str, year: int = None, quarter: int = None):

    analysis_result = analyze_root_cause(
        region=region,
        year=year,
        quarter=quarter
    )

    # Stop if no data exists
    if "error" in analysis_result:
        return analysis_result

    severity = analysis_result["root_cause"]["severity"]
    primary_cause = analysis_result["root_cause"]["primary_cause"]
    margin = analysis_result["analysis"]["margin_percentage"]

    recommendations = []

    if severity == "critical":

        if primary_cause == "material_cost":
            recommendations = [
                "Review supplier pricing and negotiate lower material costs.",
                "Identify products with unusually high material expenses.",
                "Review product pricing to protect profit margins.",
                "Consider alternative suppliers or lower-cost materials.",
                "Prioritize a detailed cost review for this region."
            ]

        elif primary_cause == "shipping_cost":
            recommendations = [
                "Review logistics and shipping provider costs.",
                "Negotiate better shipping rates.",
                "Optimize delivery routes and shipment consolidation.",
                "Review products with unusually high shipping expenses."
            ]

    elif severity == "warning":

        recommendations = [
            "Monitor the cost trend closely.",
            "Review major cost components before margins decline further.",
            "Compare this period with previous quarters.",
            "Investigate high-cost products."
        ]

    else:

        recommendations = [
            "Continue monitoring revenue and cost trends.",
            "Maintain current profitability controls.",
            "Compare future periods against the current healthy margin."
        ]

    return {
        "region": region,
        "year": year,
        "quarter": quarter,
        "margin_percentage": margin,
        "severity": severity,
        "primary_cause": primary_cause,
        "root_cause_explanation":
            analysis_result["root_cause"]["explanation"],
        "recommendations": recommendations
    }