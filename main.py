import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))

from scrapers.website_scraper import scrape_pages
from processing.data_validation import validate_records
from database.db import store_records
from crm.crm_sync import sync_records

BASE = os.path.dirname(__file__)


def load_config():
    with open(os.path.join(BASE, "config", "config.json")) as f:
        return json.load(f)


def run_pipeline():
    config = load_config()
    print(f"Target: {config['target_site']}")
    print(f"Scraping pages {config['start_page']} to {config['start_page'] + config['pages'] - 1}...")

    # 1. Scrape
    raw = scrape_pages(config["url_pattern"], config["start_page"], config["pages"], config["delay_seconds"])
    print(f"Scraped raw records: {len(raw)}")

    # 2. Validate / format / dedupe
    valid, report = validate_records(raw)
    print(f"Validation: {report}")

    # 3. Store in database
    new_count, updated_count, total = store_records(valid)
    print(f"Database: {new_count} new, {updated_count} updated, {total} total records")

    # 4. Sync to CRM (live if a HubSpot token is set, otherwise dry-run)
    result = sync_records(valid, new_count, updated_count)
    print(f"CRM sync: {result}")

    # 5. Export the scraped data
    reports_dir = os.path.join(BASE, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    df = pd.DataFrame(valid)
    df.to_csv(os.path.join(reports_dir, "scraped_products.csv"), index=False)

    quality = round(len(valid) / len(raw) * 100, 1) if raw else 0
    print("\n--- MONITORING SUMMARY ---")
    print(f"records_scraped: {len(raw)}")
    print(f"records_valid: {len(valid)}")
    print(f"duplicates_removed: {report['duplicates_removed']}")
    print(f"invalid_removed: {report['invalid_removed']}")
    print(f"data_quality_pct: {quality}")
    print(f"crm_mode: {result['mode']}")
    return {"raw": len(raw), "valid": len(valid), "report": report,
            "new": new_count, "updated": updated_count, "total": total, "sync": result, "quality": quality}


if __name__ == "__main__":
    run_pipeline()
