import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0 (portfolio project scraper; contact: github.com/Adi-dot0)"
}

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_book_page(html, page_url):
    """Parse one listing page of books.toscrape.com into raw records."""
    soup = BeautifulSoup(html, "html.parser")
    records = []
    for pod in soup.select("article.product_pod"):
        title_tag = pod.select_one("h3 a")
        title = title_tag.get("title", "").strip() if title_tag else ""
        href = title_tag.get("href", "") if title_tag else ""
        product_url = urljoin(page_url, href)

        price_tag = pod.select_one("p.price_color")
        price_text = price_tag.get_text(strip=True) if price_tag else ""

        rating_tag = pod.select_one("p.star-rating")
        rating = None
        if rating_tag:
            for cls in rating_tag.get("class", []):
                if cls in RATING_WORDS:
                    rating = RATING_WORDS[cls]

        avail_tag = pod.select_one("p.availability")
        availability = avail_tag.get_text(" ", strip=True) if avail_tag else ""

        records.append({
            "title": title,
            "price_text": price_text,
            "rating": rating,
            "availability_text": availability,
            "product_url": product_url,
        })
    return records


def scrape_pages(base_url="https://books.toscrape.com/catalogue/page-{}.html",
                 start_page=1, pages=3, delay_seconds=1):
    """Scrape listing pages with a polite delay between requests."""
    all_records = []
    for page in range(start_page, start_page + pages):
        url = base_url.format(page)
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        records = parse_book_page(response.text, url)
        print(f"Page {page}: {len(records)} records")
        all_records.extend(records)
        if page < start_page + pages - 1:
            time.sleep(delay_seconds)
    return all_records
