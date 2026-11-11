# Automated Web Scraping & CRM Synchronization

A Python system that collects product data from a website automatically, validates and de-duplicates it, stores it in a database, and syncs it to HubSpot CRM — with a Streamlit dashboard to monitor scraping and sync status.

## Business Problem
Businesses collect product, pricing and competitor information from websites manually. Manual collection wastes time and produces outdated, inconsistent data. This project automates the full flow: scrape → validate → store → sync to CRM, so the CRM stays updated without manual work.

## What it does
1. **Scrape** — collects records page by page (pagination) with a polite delay. Demo target: **books.toscrape.com**, a public website built specifically for scraping practice, so scraping it is permitted by design. Fields collected: title, price, rating, availability, product URL.
2. **Validate & format** — parses prices (£51.77 → 51.77), converts star-rating words to numbers, standardizes availability, rejects records with a missing title/price/URL, and removes duplicates using the product URL as the unique key.
3. **Store** — SQLite database with `scraped_records`, `sync_history` and `duplicate_log` tables. Re-running the pipeline updates existing records instead of duplicating them.
4. **Sync to HubSpot CRM** — records map to HubSpot Products (name, price, description with rating/availability/source URL). Duplicate check by source URL runs before creating, so a record is updated, not duplicated.
5. **Monitor** — a Streamlit dashboard shows total records, sync runs and status, duplicates, rating distribution and price summary.

## HubSpot modes (read this first)
- **Dry-run (default):** no data leaves your machine and no HubSpot account is needed. The pipeline prepares the exact sync payloads, logs the sync as `DryRun`, and writes `reports/hubspot_import.csv`, which you can import into HubSpot manually (CRM → Products → Import).
- **Live:** create a free HubSpot account, make a Private App with `crm.objects.products` read/write scopes, and set the token as an environment variable — never in code:
  ```bash
  export HUBSPOT_ACCESS_TOKEN="your-token-here"
  python main.py
  ```
  The code then creates/updates real products in your HubSpot account through `crm/hubspot_api.py`.

## Tech Stack
Python, Requests, BeautifulSoup, Selenium (ready module for JavaScript-heavy sites), Pandas, SQLite, HubSpot API, Streamlit, GitHub

## Folder Structure
```
automated-web-scraping-crm-sync/
  main.py
  requirements.txt
  config/config.json
  scrapers/    website_scraper.py, selenium_handler.py
  processing/  data_validation.py
  database/    schema.sql, db.py
  crm/         hubspot_api.py, crm_sync.py
  dashboard/   app.py (Streamlit)
  tests/       test_scraper.py, test_validation.py, test_crm_sync.py, fixtures/
  reports/     scraped_products.csv, hubspot_import.csv
```

## How to Run
```bash
pip install -r requirements.txt
python main.py                      # scrape + validate + store + sync (dry-run)
streamlit run dashboard/app.py      # monitoring dashboard
```

## Verified Results (live run, 11 November 2026)
- Scraped **60 real book records** from pages 1–3 of books.toscrape.com
- Validation: 60 valid, 0 invalid, 0 duplicates on the first run (the site data is clean; the duplicate/invalid rules are proven in the unit tests with planted bad rows)
- Database: 60 records stored. **Second run: 0 new, 60 updated** — the duplicate protection works live: re-scraping updates records instead of duplicating them
- CRM sync (dry-run): 60 records prepared, `hubspot_import.csv` written with 60 rows, both runs logged in `sync_history` as `DryRun`
- Ratings distribution: 1★ 15, 2★ 8, 3★ 13, 4★ 10, 5★ 14 | Prices: £12.84 – £57.31, average £35.00
- All **6 unit tests pass** (parser on a saved page fixture, price cleaning, dedupe/validation, HubSpot payload mapping, database insert/update)

## Tests
```bash
pip install pytest
pytest tests/ -v
```
Tests run offline — the scraper is tested against a saved HTML page in `tests/fixtures/`.

## Scraping responsibility
Only scrape websites that permit it (check the site's terms and robots rules), keep request rates polite (this project waits 1 second between pages and identifies itself in the User-Agent), and never collect personal data without a lawful basis. The demo target is a site created for scraping practice.

## Limitations (honest)
- Live HubSpot sync needs your own free HubSpot account and Private App token; by default the project runs in dry-run mode and nothing is sent anywhere.
- The Selenium module is provided for JavaScript-heavy websites but is not used for the demo site, which is plain HTML.
- The scraper's parser is written for the demo site's page structure; a different website needs its selectors updated in `scrapers/website_scraper.py`.
- Prices are collected in GBP because the demo site prices in pounds.
