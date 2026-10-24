
import re

from backend.analytics import (
    get_total_revenue,
    get_top_product,
    get_monthly_revenue,
    get_top_region,
    compare_months,
)


MONTHS = {
    "january": "01",
    "jan": "01",
    "february": "02",
    "feb": "02",
    "march": "03",
    "mar": "03",
    "april": "04",
    "apr": "04",
    "may": "05",
    "june": "06",
    "jun": "06",
    "july": "07",
    "jul": "07",
    "august": "08",
    "aug": "08",
    "september": "09",
    "sep": "09",
    "october": "10",
    "oct": "10",
    "november": "11",
    "nov": "11",
    "december": "12",
    "dec": "12",
}


def extract_months(question):
    text = question.lower()
    found = []

    pattern = (
        r"\b(january|jan|february|feb|march|mar|april|apr|"
        r"may|june|jun|july|jul|august|aug|september|sep|"
        r"october|oct|november|nov|december|dec)"
        r"\s+(20\d{2})\b"
    )

    for match in re.finditer(pattern, text):
        month_name = match.group(1)
        year = match.group(2)
        found.append(f"{year}-{MONTHS[month_name]}")

    return found


def answer_question(question):
    if not question or not question.strip():
        return {
            "status": "error",
            "message": "Please enter a question.",
        }

    text = question.lower().strip()

    # Month comparison must be checked before general revenue.
    comparison_words = [
        "compare", "change", "difference",
        "increased", "decreased", "growth",
        "percentage change", "from", "to",
    ]

    months = extract_months(text)

    if (
        len(months) >= 2
        and any(word in text for word in comparison_words)
    ):
        result = compare_months(months[0], months[1])

        if "error" in result:
            return {
                "status": "error",
                "message": result["error"],
            }

        return {
            "status": "success",
            "intent": "month_comparison",
            "question": question,
            "answer": (
                f"Revenue changed from ₹{result['revenue_a']:,.2f} "
                f"in {result['month_a']} to "
                f"₹{result['revenue_b']:,.2f} in {result['month_b']}. "
                f"The difference was ₹{result['difference']:,.2f} "
                f"({result['percentage_change']}% change)."
                if result["percentage_change"] is not None
                else (
                    f"Revenue changed by ₹{result['difference']:,.2f}. "
                    "Percentage change is undefined because the "
                    "starting revenue was zero."
                )
            ),
            "evidence": result,
        }

    if any(word in text for word in [
        "top product", "highest revenue product",
        "best-selling product", "best selling product",
        "product generated the most", "product generated the highest",
        "which product", "highest product",
    ]):
        result = get_top_product()

        if result is None:
            return {
                "status": "error",
                "message": "No eligible product revenue found.",
            }

        return {
            "status": "success",
            "intent": "top_product",
            "question": question,
            "answer": (
                f"{result['product']} generated the highest "
                f"eligible revenue at ₹{result['revenue']:,.2f}."
            ),
            "evidence": result,
        }

    if any(word in text for word in [
        "top region", "best region", "highest region",
        "region performed best", "region generated the most",
        "which region",
    ]):
        result = get_top_region()

        if result is None:
            return {
                "status": "error",
                "message": "No eligible regional revenue found.",
            }

        return {
            "status": "success",
            "intent": "top_region",
            "question": question,
            "answer": (
                f"{result['region']} is the top region by eligible "
                f"revenue, with ₹{result['revenue']:,.2f}."
            ),
            "evidence": result,
        }

    if any(word in text for word in [
        "monthly", "month-wise", "month wise",
        "trend", "over time", "each month",
    ]):
        result = get_monthly_revenue()

        if not result:
            return {
                "status": "error",
                "message": "No monthly revenue data found.",
            }

        highest = max(result, key=lambda item: item["revenue"])

        return {
            "status": "success",
            "intent": "monthly_revenue",
            "question": question,
            "answer": (
                f"Revenue peaked in {highest['month']} at "
                f"₹{highest['revenue']:,.2f}. "
                f"The monthly results contain {len(result)} months."
            ),
            "evidence": {"months": result},
        }

    if any(word in text for word in [
        "total revenue", "overall revenue",
        "total sales", "revenue generated",
        "how much revenue", "sales revenue",
    ]):
        result = get_total_revenue()

        return {
            "status": "success",
            "intent": "total_revenue",
            "question": question,
            "answer": (
                f"Total eligible net revenue is "
                f"₹{result['total_revenue']:,.2f}, across "
                f"{result['eligible_transactions']} eligible transactions."
            ),
            "evidence": result,
        }

    return {
        "status": "unsupported",
        "question": question,
        "message": (
            "I couldn't map that question to a supported analytics "
            "operation. Try asking about total revenue, the top product, "
            "monthly trends, the top region, or a comparison between "
            "two months."
        ),
    }
