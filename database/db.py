import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE, "scraping.db")
SCHEMA = os.path.join(BASE, "database", "schema.sql")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA) as f:
        conn.executescript(f.read())
    return conn


def store_records(records):
    """Insert new records, update price/last_seen for existing ones.

    Returns (new_count, updated_count) using product_url as unique key.
    """
    conn = get_connection()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_count, updated_count = 0, 0
    for r in records:
        existing = conn.execute(
            "SELECT record_id FROM scraped_records WHERE product_url = ?", (r["product_url"],)
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE scraped_records SET price = ?, rating = ?, availability = ?, last_seen = ? WHERE product_url = ?",
                (r["price"], r["rating"], r["availability"], now, r["product_url"]),
            )
            updated_count += 1
        else:
            conn.execute(
                "INSERT INTO scraped_records (title, price, rating, availability, product_url, first_seen, last_seen) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (r["title"], r["price"], r["rating"], r["availability"], r["product_url"], now, now),
            )
            new_count += 1
    conn.commit()
    total = conn.execute("SELECT COUNT(*) FROM scraped_records").fetchone()[0]
    conn.close()
    return new_count, updated_count, total


def log_duplicate(record):
    conn = get_connection()
    conn.execute(
        "INSERT INTO duplicate_log (product_url, title, detected_time) VALUES (?, ?, ?)",
        (record["product_url"], record["title"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()


def log_sync(records_synced, new_records, updated_records, status, error=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO sync_history (sync_time, records_synced, new_records, updated_records, sync_status, error_message) VALUES (?, ?, ?, ?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), records_synced, new_records, updated_records, status, error),
    )
    conn.commit()
    conn.close()
