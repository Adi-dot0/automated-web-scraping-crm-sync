import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

os.environ.pop("HUBSPOT_ACCESS_TOKEN", None)  # force dry-run mode in tests

from crm.hubspot_api import record_to_hubspot_properties
from database.db import store_records, get_connection


def test_hubspot_payload():
    record = {"title": "Book One", "price": 51.77, "rating": 3,
              "availability": "In stock", "product_url": "http://x/1"}
    props = record_to_hubspot_properties(record)
    assert props["name"] == "Book One"
    assert props["price"] == "51.77"
    assert "http://x/1" in props["description"]


def test_store_records_dedupes_on_second_run(tmp_path, monkeypatch):
    import database.db as db
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))
    records = [{"title": "A", "price": 10.0, "rating": 4, "availability": "In stock", "product_url": "http://x/1"}]
    new, updated, total = db.store_records(records)
    assert (new, updated, total) == (1, 0, 1)
    new2, updated2, total2 = db.store_records(records)
    assert (new2, updated2, total2) == (0, 1, 1)
