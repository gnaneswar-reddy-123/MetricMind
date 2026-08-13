from fastapi import APIRouter
from app.services.semantic_service import get_metric_summary

router = APIRouter()


@router.get("/governance-audit")
def governance_audit():
    first_result = get_metric_summary("revenue")
    second_result = get_metric_summary("revenue")

    first_value = first_result["value"]
    second_value = second_result["value"]

    passed = first_value == second_value

    return {
        "audit_name": "Governed Metric Consistency Audit",
        "metric": "revenue",
        "first_result": first_value,
        "second_result": second_value,
        "passed": passed,
        "message": (
            "Governance audit passed. The governed metric returned "
            "the same result consistently."
            if passed
            else
            "Governance audit failed. The results were inconsistent."
        )
    }