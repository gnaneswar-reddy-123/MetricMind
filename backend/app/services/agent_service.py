from app.services.semantic_service import get_metric_summary


REGIONS = [
    "North America",
    "South America",
    "Europe",
    "Asia",
    "Africa"
]


def analyze_question(question: str):
    question_lower = question.lower()

    metric = None

    if "revenue" in question_lower or "sales" in question_lower:
        metric = "revenue"
    elif "cost" in question_lower:
        metric = "cost"
    elif "profit" in question_lower:
        metric = "profit"
    elif "margin" in question_lower:
        metric = "margin"

    if not metric:
        return {
            "error": "I could not identify a supported metric.",
            "supported_metrics": [
                "revenue",
                "cost",
                "profit",
                "margin"
            ]
        }

    region = None

    for item in REGIONS:
        if item.lower() in question_lower:
            region = item
            break

    result = get_metric_summary(metric, region)

    return {
        "question": question,
        "understood_metric": metric,
        "understood_region": region,
        "result": result
    }