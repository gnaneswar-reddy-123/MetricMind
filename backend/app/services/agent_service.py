from app.services.semantic_service import get_metric_summary
from app.services.root_cause_service import analyze_root_cause


# User-friendly region names.
# "Asia" is accepted and semantic_service maps it to "Asia Pacific".
REGIONS = [
    "North America",
    "South America",
    "Asia Pacific",
    "Europe",
    "Asia"
]


def analyze_question(question: str):
    question_lower = question.lower()

    # -----------------------------
    # 1. Detect the governed metric
    # -----------------------------
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

    # -----------------------------
    # 2. Detect the region
    # -----------------------------
    region = None

    for item in REGIONS:
        if item.lower() in question_lower:
            region = item
            break

    # -----------------------------
    # 3. Detect the year
    # -----------------------------
    year = None

    for possible_year in range(2020, 2031):
        if str(possible_year) in question_lower:
            year = possible_year
            break

    # -----------------------------
    # 4. Detect the quarter
    # -----------------------------
    quarter = None

    for possible_quarter in range(1, 5):
        if (
            f"q{possible_quarter}" in question_lower
            or f"quarter {possible_quarter}" in question_lower
        ):
            quarter = possible_quarter
            break

    # -----------------------------
    # 5. Detect diagnostic questions
    # -----------------------------
    diagnostic_keywords = [
        "why",
        "drop",
        "dropped",
        "decline",
        "declined",
        "decrease",
        "decreased",
        "root cause",
        "reason"
    ]

    is_diagnostic_question = any(
        keyword in question_lower
        for keyword in diagnostic_keywords
    )

    # ----------------------------------------
    # 6. Multi-step analysis for margin issues
    # ----------------------------------------
    if (
        metric == "margin"
        and is_diagnostic_question
        and region
    ):
        root_cause_result = analyze_root_cause(
            region=region,
            year=year,
            quarter=quarter
        )

        return {
            "question": question,
            "workflow": "multi_step_margin_analysis",
            "understood_metric": metric,
            "understood_region": region,
            "understood_year": year,
            "understood_quarter": quarter,
            "steps": [
                "Detected governed metric: margin",
                "Detected business region",
                "Detected requested time period",
                "Calculated margin and cost breakdown",
                "Identified primary cost contributor"
            ],
            "result": root_cause_result
        }

    # ----------------------------------------
    # 7. Normal governed metric query
    # ----------------------------------------
    result = get_metric_summary(metric, region)

    return {
        "question": question,
        "workflow": "governed_metric_query",
        "understood_metric": metric,
        "understood_region": region,
        "result": result
    }