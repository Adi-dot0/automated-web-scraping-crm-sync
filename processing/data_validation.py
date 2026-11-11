import re


def clean_price(price_text):
    """'£51.77' -> 51.77 ; returns None when no number is found."""
    if price_text is None:
        return None
    match = re.search(r"[\d]+\.[\d]+|[\d]+", str(price_text).replace(",", ""))
    return float(match.group()) if match else None


def validate_records(raw_records):
    """Format and validate scraped records, remove duplicates.

    Returns (valid_records, report). A record is valid when it has a
    title, a parsed price and a product URL. Duplicates are detected
    by product URL (the unique key of a record).
    """
    report = {"rows_in": len(raw_records), "invalid_removed": 0, "duplicates_removed": 0}
    valid = []
    seen_urls = set()

    for r in raw_records:
        title = (r.get("title") or "").strip()
        url = (r.get("product_url") or "").strip()
        price = clean_price(r.get("price_text"))
        if not title or not url or price is None:
            report["invalid_removed"] += 1
            continue
        if url in seen_urls:
            report["duplicates_removed"] += 1
            continue
        seen_urls.add(url)
        availability = "In stock" if "in stock" in (r.get("availability_text") or "").lower() else "Out of stock"
        valid.append({
            "title": title,
            "price": price,
            "rating": r.get("rating"),
            "availability": availability,
            "product_url": url,
        })

    report["rows_out"] = len(valid)
    return valid, report
