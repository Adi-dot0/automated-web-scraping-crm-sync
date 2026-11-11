import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scrapers.website_scraper import parse_book_page

FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "sample_page.html")


def load_fixture():
    with open(FIXTURE, encoding="utf-8") as f:
        return f.read()


def test_parse_finds_all_products():
    records = parse_book_page(load_fixture(), "https://books.toscrape.com/catalogue/page-1.html")
    assert len(records) == 3


def test_parse_fields():
    records = parse_book_page(load_fixture(), "https://books.toscrape.com/catalogue/page-1.html")
    first = records[0]
    assert first["title"] == "Book One"
    assert first["rating"] == 3
    assert "51.77" in first["price_text"]
    assert first["product_url"].endswith("book-one_1/index.html")
