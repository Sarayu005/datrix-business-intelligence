import json
from pathlib import Path

from backend.analytics import (
    get_total_revenue,
    get_top_product,
    get_monthly_revenue,
    get_top_region,
    compare_months,
)
from backend.llm_interpreter import interpret_question


def get_quality_report():
    report_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "data_quality_report.json"
    )

    if not report_path.exists():
        return {}

    try:
        with open(report_path, "r", encoding="utf-8") as file:
            report = json.load(file)

        return report if isinstance(report, dict) else {}

    except (OSError, json.JSONDecodeError):
        return {}


def find_quality_value(report, possible_names):
    if isinstance(report, dict):
        for name in possible_names:
            if name in report and report[name] is not None:
                return report[name]

        for value in report.values():
            result = find_quality_value(value, possible_names)

            if result is not None:
                return result

    elif isinstance(report, list):
        for item in report:
            result = find_quality_value(item, possible_names)

            if result is not None:
                return result

    return None


def answer_question_with_ai(question):
    if not question or not question.strip():
        return {
            "status": "error",
            "message": "Please enter a question.",
        }

    parsed = interpret_question(question)
    intent = parsed["intent"]
    chart_data = None

    if intent == "unsupported":
        return {
            "status": "unsupported",
            "question": question,
            "message": (
                "I can answer questions about total revenue, the top "
                "product, the top region, monthly trends, comparisons "
                "between two months, and data quality."
            ),
        }

    if intent == "total_revenue":
        evidence = get_total_revenue()

        answer = (
            f"Total eligible net revenue is "
            f"₹{evidence['total_revenue']:,.2f}, across "
            f"{evidence['eligible_transactions']} eligible transactions."
        )

    elif intent == "top_product":
        evidence = get_top_product()

        if evidence is None:
            return {
                "status": "error",
                "message": "No eligible product revenue found.",
            }

        answer = (
            f"{evidence['product']} generated the highest "
            f"eligible revenue at ₹{evidence['revenue']:,.2f}."
        )

        chart_data = {
            "type": "bar",
            "title": "Top Product by Revenue",
            "data": [
                {
                    "label": evidence["product"],
                    "revenue": evidence["revenue"],
                }
            ],
        }

    elif intent == "top_region":
        evidence = get_top_region()

        if evidence is None:
            return {
                "status": "error",
                "message": "No eligible regional revenue found.",
            }

        answer = (
            f"{evidence['region']} is the top region by eligible "
            f"revenue, with ₹{evidence['revenue']:,.2f}."
        )

        chart_data = {
            "type": "bar",
            "title": "Top Region by Revenue",
            "data": [
                {
                    "label": evidence["region"],
                    "revenue": evidence["revenue"],
                }
            ],
        }

    elif intent == "monthly_revenue":
        evidence = {"months": get_monthly_revenue()}

        if not evidence["months"]:
            return {
                "status": "error",
                "message": "No monthly revenue data found.",
            }

        highest = max(
            evidence["months"],
            key=lambda item: item["revenue"],
        )

        answer = (
            f"Revenue peaked in {highest['month']} at "
            f"₹{highest['revenue']:,.2f}."
        )

        chart_data = {
            "type": "line",
            "title": "Monthly Revenue Trend",
            "data": [
                {
                    "label": item["month"],
                    "revenue": item["revenue"],
                }
                for item in evidence["months"]
            ],
        }

    elif intent == "month_comparison":
        evidence = compare_months(
            parsed["month_a"],
            parsed["month_b"],
        )

        if "error" in evidence:
            return {
                "status": "error",
                "message": evidence["error"],
            }

        difference = evidence["difference"]
        percentage = evidence["percentage_change"]

        if percentage is None:
            change_text = (
                "The percentage change is undefined because "
                "the starting revenue was zero."
            )
        else:
            change_text = f"a {percentage}% change"

        answer = (
            f"Revenue was ₹{evidence['revenue_a']:,.2f} in "
            f"{evidence['month_a']} and "
            f"₹{evidence['revenue_b']:,.2f} in "
            f"{evidence['month_b']}. The difference was "
            f"₹{difference:,.2f}, representing {change_text}."
        )

        chart_data = {
            "type": "bar",
            "title": "Monthly Revenue Comparison",
            "data": [
                {
                    "label": evidence["month_a"],
                    "revenue": evidence["revenue_a"],
                },
                {
                    "label": evidence["month_b"],
                    "revenue": evidence["revenue_b"],
                },
            ],
        }

    elif intent in (
        "eligible_rows",
        "flagged_rows",
        "exclusion_reasons",
        "revenue_basis",
        "source_rows",
    ):
        report = get_quality_report()

        if not report:
            return {
                "status": "error",
                "message": (
                    "The data-quality report is unavailable. "
                    "Check data/data_quality_report.json."
                ),
            }

        if intent == "source_rows":
            count = find_quality_value(
                report,
                [
                    "original_rows",
                    "source_rows",
                    "total_rows",
                    "source_row_count",
                    "row_count",
                    "stored_rows",
                ],
            )

            if count is None:
                answer = (
                    "The source row count is not available in "
                    "the data-quality report."
                )
            else:
                answer = f"The source dataset contains {count} rows."

            evidence = {
                "source_rows": count,
            }

        elif intent == "eligible_rows":
            count = find_quality_value(
                report,
                [
                    "eligible_for_revenue",
                    "eligible_rows",
                    "eligible_transactions",
                    "eligible_row_count",
                ],
            )

            if count is None:
                answer = (
                    "The eligible row count is not available in "
                    "the data-quality report."
                )
            else:
                answer = (
                    f"{count} rows are eligible for revenue calculations."
                )

            evidence = {
                "eligible_rows": count,
            }

        elif intent == "flagged_rows":
            count = find_quality_value(
                report,
                [
                    "rows_with_quality_flags",
                    "flagged_rows",
                    "invalid_rows",
                    "flagged_row_count",
                ],
            )

            if count is None:
                answer = (
                    "The flagged row count is not available in "
                    "the data-quality report."
                )
            else:
                answer = (
                    f"{count} records were flagged for "
                    "data-quality issues."
                )

            evidence = {
                "flagged_rows": count,
            }

        elif intent == "exclusion_reasons":
            policy = find_quality_value(
                report,
                ["revenue_policy", "eligibility_policy", "policy"],
            )

            if not policy:
                policy = (
                    "Only completed transactions with valid required "
                    "fields, positive quantities and unit prices, valid "
                    "discounts, and unique transaction IDs are included "
                    "in revenue calculations."
                )

            answer = (
                "Records may be excluded from revenue calculations "
                "if they fail the revenue eligibility rules. These can "
                "include invalid dates, missing products, non-completed "
                "statuses, non-positive quantities or prices, invalid "
                "discounts, or duplicate transaction IDs. "
                "A flagged record is not necessarily excluded. "
                f"Eligibility policy: {policy}"
            )

            evidence = {
                "revenue_policy": policy,
                "quality_report": report,
            }

        else:  # revenue_basis
            revenue_data = get_total_revenue()

            policy = find_quality_value(
                report,
                ["revenue_policy", "eligibility_policy", "policy"],
            )

            answer = (
                "Net revenue is calculated as quantity multiplied by "
                "unit price, minus the discount amount. Only eligible "
                "transactions are included in the calculation. "
                f"Total eligible net revenue is "
                f"₹{revenue_data['total_revenue']:,.2f}, across "
                f"{revenue_data['eligible_transactions']} eligible "
                "transactions."
            )

            if policy:
                answer += f" Eligibility policy: {policy}"

            evidence = {
                "total_revenue": revenue_data["total_revenue"],
                "eligible_transactions": (
                    revenue_data["eligible_transactions"]
                ),
                "revenue_policy": policy,
            }

    else:
        return {
            "status": "unsupported",
            "question": question,
            "message": "That analytics operation is not supported.",
        }

    return {
        "status": "success",
        "source": "Gemini intent + verified analytics",
        "intent": intent,
        "question": question,
        "answer": answer,
        "evidence": evidence,
        "chart_data": chart_data,
    }