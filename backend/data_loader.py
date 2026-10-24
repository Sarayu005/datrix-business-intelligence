
import json
import re
from pathlib import Path

import pandas as pd

from backend.database import (
    DB_PATH,
    DATA_DIR,
    get_connection,
    initialize_database,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = DATA_DIR / "sales_data.csv"
REPORT_PATH = DATA_DIR / "data_quality_report.json"


def normalize_column(name):
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


COLUMN_ALIASES = {
    "transactionid": "transaction_id",
    "orderdate": "order_date",
    "product": "product",
    "category": "category",
    "region": "region",
    "saleschannel": "sales_channel",
    "quantity": "quantity",
    "unitprice": "unit_price",
    "discountamount": "discount_amount",
    "status": "status",
}


def load_csv():
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"CSV not found: {CSV_PATH}\n"
            "Place sales_data.csv inside the data folder."
        )

    df = pd.read_csv(CSV_PATH)

    normalized = {
        normalize_column(column): column
        for column in df.columns
    }

    missing = [
        key for key in COLUMN_ALIASES
        if key not in normalized
    ]

    if missing:
        raise ValueError(
            "CSV is missing required columns: "
            + ", ".join(missing)
            + f". Found: {list(df.columns)}"
        )

    df = df.rename(columns={
        normalized[source]: destination
        for source, destination in COLUMN_ALIASES.items()
    })

    return df[list(COLUMN_ALIASES.values())].copy()


def clean_and_validate(df):
    original_count = len(df)

    # Standardize text fields without hiding missing values.
    text_columns = [
        "transaction_id", "product", "category",
        "region", "sales_channel", "status"
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()
        df[column] = df[column].replace("", pd.NA)

    # Parse dates in the supplied day-month-year format.
    parsed_dates = pd.to_datetime(
        df["order_date"],
        dayfirst=True,
        errors="coerce"
    )
    df["order_date"] = parsed_dates.dt.strftime("%Y-%m-%d")

    # Invalid numbers become missing, not zero.
    for column in [
        "quantity", "unit_price", "discount_amount"
    ]:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    flags = [[] for _ in range(len(df))]

    def flag_rows(mask, message):
        mask = mask.fillna(False)

        for index in range(len(df)):
            if mask.iloc[index]:
                flags[index].append(message)

    # Identify every occurrence of a duplicated ID.
    duplicate_id = (
        df["transaction_id"].notna()
        & df["transaction_id"].duplicated(keep=False)
    )
    flag_rows(duplicate_id, "duplicate_transaction_id")

    flag_rows(
        df["transaction_id"].isna(),
        "missing_transaction_id"
    )
    flag_rows(
        df["order_date"].isna(),
        "invalid_or_missing_date"
    )
    flag_rows(
        df["product"].isna(),
        "missing_product"
    )
    flag_rows(
        df["quantity"].isna(),
        "missing_or_invalid_quantity"
    )
    flag_rows(
        df["quantity"].notna() & (df["quantity"] < 0),
        "negative_quantity"
    )
    flag_rows(
        df["quantity"].eq(0),
        "zero_quantity"
    )
    flag_rows(
        df["unit_price"].isna(),
        "missing_or_invalid_unit_price"
    )
    flag_rows(
        df["unit_price"].notna() & (df["unit_price"] < 0),
        "negative_unit_price"
    )
    flag_rows(
        df["unit_price"].eq(0),
        "zero_unit_price_review"
    )
    flag_rows(
        df["discount_amount"].isna(),
        "missing_or_invalid_discount"
    )
    flag_rows(
        df["discount_amount"].notna()
        & (df["discount_amount"] < 0),
        "negative_discount"
    )
    flag_rows(
        df["status"].isna(),
        "missing_status"
    )

    # Missing discounts are not assumed to be zero.
    gross = df["quantity"] * df["unit_price"]

    flag_rows(
        gross.notna()
        & df["discount_amount"].notna()
        & (df["discount_amount"] > gross),
        "discount_exceeds_gross"
    )

    normalized_status = df["status"].str.lower()

    flag_rows(
        normalized_status.eq("returned"),
        "returned_transaction"
    )

    flag_rows(
        normalized_status.notna()
        & ~normalized_status.isin(["completed", "returned"]),
        "unknown_status"
    )

    # Conservative policy: only clearly valid completed rows
    # contribute to revenue. Suspicious rows remain in the DB.
    eligible = (
        (normalized_status == "completed")
        & df["transaction_id"].notna()
        & ~duplicate_id
        & df["order_date"].notna()
        & df["product"].notna()
        & df["quantity"].notna()
        & (df["quantity"] > 0)
        & df["unit_price"].notna()
        & (df["unit_price"] > 0)
        & df["discount_amount"].notna()
        & (df["discount_amount"] >= 0)
        & gross.notna()
        & (df["discount_amount"] <= gross)
    ).fillna(False)

    df["revenue"] = (
        gross - df["discount_amount"]
    ).where(eligible, None)

    df["is_eligible_for_revenue"] = eligible.astype(int)

    df["quality_flags"] = [
        ";".join(row_flags) for row_flags in flags
    ]

    # Store SQLite-friendly missing values.
    df["order_date"] = df["order_date"].astype(object)
    df = df.astype(object).where(pd.notna(df), None)

    return df, original_count


def import_sales_data():
    initialize_database()

    raw_df = load_csv()
    df, original_count = clean_and_validate(raw_df)

    columns = [
        "transaction_id", "order_date", "product",
        "category", "region", "sales_channel",
        "quantity", "unit_price", "discount_amount",
        "status", "revenue", "is_eligible_for_revenue",
        "quality_flags"
    ]

    placeholders = ", ".join(["?"] * len(columns))
    column_sql = ", ".join(columns)

    rows = [
        tuple(row[column] for column in columns)
        for _, row in df.iterrows()
    ]

    # Replace the previous import in a single transaction.
    # A failed import rolls back instead of leaving partial data.
    with get_connection() as conn:
        conn.execute("DELETE FROM sales_transactions")

        conn.executemany(
            f"""
            INSERT INTO sales_transactions ({column_sql})
            VALUES ({placeholders})
            """,
            rows
        )

        total_stored = conn.execute(
            "SELECT COUNT(*) FROM sales_transactions"
        ).fetchone()[0]

        eligible_count = conn.execute(
            """
            SELECT COUNT(*) FROM sales_transactions
            WHERE is_eligible_for_revenue = 1
            """
        ).fetchone()[0]

        flagged_count = conn.execute(
            """
            SELECT COUNT(*) FROM sales_transactions
            WHERE quality_flags != ''
            """
        ).fetchone()[0]

        total_revenue = conn.execute(
            """
            SELECT COALESCE(SUM(revenue), 0)
            FROM sales_transactions
            WHERE is_eligible_for_revenue = 1
            """
        ).fetchone()[0]

    report = {
        "source_file": CSV_PATH.name,
        "original_rows": original_count,
        "stored_rows": total_stored,
        "eligible_for_revenue": eligible_count,
        "rows_with_quality_flags": flagged_count,
        "excluded_from_revenue": total_stored - eligible_count,
        "eligible_net_revenue": round(total_revenue, 2),
        "database": str(DB_PATH),
        "revenue_policy": (
            "Completed transactions only; positive quantity "
            "and unit price; valid nonnegative discount; "
            "valid date and product; unique transaction ID."
        )
    }

    REPORT_PATH.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )

    print("\nSALES DATA IMPORT COMPLETE")
    print("-" * 35)

    for key, value in report.items():
        print(f"{key}: {value}")

    print(f"\nQuality report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    import_sales_data()
