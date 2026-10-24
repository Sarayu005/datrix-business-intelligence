
from pathlib import Path
import json
import re

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.question_service import answer_question
from pydantic import BaseModel
from backend.ai_service import answer_question_with_ai
from backend.analytics import (
    get_total_revenue,
    get_top_product,
    get_monthly_revenue,
    get_top_region,
    compare_months,
    get_product_revenue,
    get_region_revenue,
)

app = FastAPI(
    title="SalesIQ API",
    description="Database-backed business intelligence analytics",
    version="1.0.0",
)

# Allows the local frontend to call this API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUALITY_REPORT_PATH = (
    PROJECT_ROOT / "data" / "data_quality_report.json"
)


@app.get("/")
def home():
    return {
        "app": "SalesIQ",
        "message": "Sales analytics API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    # A real DB check, not just an HTTP server check.
    from backend.database import get_connection

    try:
        with get_connection() as conn:
            conn.execute("SELECT 1").fetchone()
        return {"status": "healthy", "database": "connected"}
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Database is unavailable",
        ) from exc


@app.get("/analytics/revenue")
def total_revenue():
    return get_total_revenue()


@app.get("/analytics/top-product")
def top_product():
    result = get_top_product()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="No eligible product revenue found",
        )

    return result


@app.get("/analytics/monthly")
def monthly_revenue():
    return {"months": get_monthly_revenue()}


@app.get("/analytics/top-region")
def top_region():
    result = get_top_region()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="No eligible regional revenue found",
        )

    return result


@app.get("/analytics/compare")
def monthly_comparison(
    month_a: str = Query(
        ...,
        description="First month in YYYY-MM format",
        examples=["2026-01"],
    ),
    month_b: str = Query(
        ...,
        description="Second month in YYYY-MM format",
        examples=["2026-02"],
    ),
):
    # Validate the format before querying the database.
    pattern = r"^\d{4}-(0[1-9]|1[0-2])$"

    if not re.fullmatch(pattern, month_a):
        raise HTTPException(
            status_code=400,
            detail="month_a must use YYYY-MM format",
        )

    if not re.fullmatch(pattern, month_b):
        raise HTTPException(
            status_code=400,
            detail="month_b must use YYYY-MM format",
        )

    result = compare_months(month_a, month_b)

    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail=result["error"],
        )

    return result


@app.get("/analytics/data-quality")
def data_quality():
    if not QUALITY_REPORT_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Data quality report not found. Import the CSV first.",
        )

    return json.loads(
        QUALITY_REPORT_PATH.read_text(encoding="utf-8")
    )

class QuestionRequest(BaseModel):
    question: str


@app.get("/analytics/products")
def product_revenue():
    return {
        "products": get_product_revenue()
    }


@app.get("/analytics/regions")
def region_revenue():
    return {
        "regions": get_region_revenue()
    }

@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        return answer_question(request.question)
    except Exception as exc:
        # Log technical details in the terminal, but do not
        # expose internal database errors to the user.
        print(f"Question processing failed: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Unable to process the question right now.",
        ) from exc
@app.post("/ask-ai")
def ask_question_with_ai(request: QuestionRequest):
    try:
        return answer_question_with_ai(request.question)
    except Exception as exc:
        print(f"AI question processing failed: {exc}")

        raise HTTPException(
            status_code=502,
            detail=(
                "The AI service could not process the question. "
                "Check the API key, model availability, and quota."
            ),
        ) from exc