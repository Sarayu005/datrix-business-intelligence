
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "sales.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sales_transactions (
                row_id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT,
                order_date TEXT,
                product TEXT,
                category TEXT,
                region TEXT,
                sales_channel TEXT,
                quantity INTEGER,
                unit_price REAL,
                discount_amount REAL,
                status TEXT,
                revenue REAL,
                is_eligible_for_revenue INTEGER NOT NULL DEFAULT 0,
                quality_flags TEXT DEFAULT ''
            )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_sales_date
            ON sales_transactions(order_date)
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_sales_product
            ON sales_transactions(product)
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_sales_region
            ON sales_transactions(region)
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_sales_transaction_id
            ON sales_transactions(transaction_id)
        """)


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized at: {DB_PATH}")
