from app.services.semantic_service import (
    get_metric_summary,
    get_available_metrics
)


def test_revenue_is_consistent():
    first_result = get_metric_summary("revenue")
    second_result = get_metric_summary("revenue")

    assert first_result["value"] == second_result["value"]


def test_invalid_metric_is_rejected():
    result = get_metric_summary("salary")

    assert "error" in result
    assert "not allowed" in result["error"]


def test_asia_region_mapping():
    result = get_metric_summary("revenue", "asia")

    assert result["region"] == "Asia Pacific"
    assert result["value"] > 0


def test_approved_metrics_are_available():
    metrics = get_available_metrics()

    assert "revenue" in metrics
    assert "cost" in metrics
    assert "profit" in metrics
    assert "margin" in metrics