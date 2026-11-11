import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from processing.data_validation import clean_price, validate_records


def raw_sample():
    return [
        {"title": "A", "price_text": "£10.00", "rating": 4, "availability_text": "In stock", "product_url": "http://x/1"},
        {"title": "A copy", "price_text": "£10.00", "rating": 4, "availability_text": "In stock", "product_url": "http://x/1"},
        {"title": "", "price_text": "£5.00", "rating": 2, "availability_text": "In stock", "product_url": "http://x/2"},
        {"title": "B", "price_text": "no price", "rating": 2, "availability_text": "In stock", "product_url": "http://x/3"},
    ]


def test_clean_price():
    assert clean_price("£51.77") == 51.77
    assert clean_price("abc") is None


def test_validate_removes_duplicates_and_invalid():
    valid, report = validate_records(raw_sample())
    assert report["duplicates_removed"] == 1
    assert report["invalid_removed"] == 2
    assert len(valid) == 1
    assert valid[0]["price"] == 10.00
    assert valid[0]["availability"] == "In stock"
