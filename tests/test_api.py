
from fastapi.testclient import TestClient

from backend.api import app
from backend.question_service import answer_question

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_total_revenue_question():
    result = answer_question("What is our total revenue?")

    assert result["status"] == "success"
    assert result["intent"] == "total_revenue"
    assert result["evidence"]["total_revenue"] == 1439200.0


def test_top_product_question():
    result = answer_question(
        "Which product generated the highest revenue?"
    )

    assert result["status"] == "success"
    assert result["evidence"]["product"] == "Monitor"
    assert result["evidence"]["revenue"] == 473000.0


def test_month_comparison_question():
    response = client.post(
        "/ask",
        json={
            "question": "Compare January 2026 with February 2026"
        },
    )

    assert response.status_code == 200

    result = response.json()
    assert result["status"] == "success"
    assert result["evidence"]["difference"] == 24350.0
    assert result["evidence"]["percentage_change"] == 11.58


def test_unsupported_question():
    result = answer_question("What is the weather today?")

    assert result["status"] == "unsupported"
    assert "message" in result
    assert "evidence" not in result


def test_empty_question():
    result = answer_question("   ")

    assert result["status"] == "error"
    assert result["message"] == "Please enter a question."


def test_invalid_month_format():
    response = client.get(
        "/analytics/compare",
        params={
            "month_a": "January",
            "month_b": "2026-02",
        },
    )

    assert response.status_code == 400
