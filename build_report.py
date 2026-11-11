from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors

OUT = "Automated_Web_Scraping_CRM_Sync_Project_Report.pdf"
styles = getSampleStyleSheet()
title = ParagraphStyle("title2", parent=styles["Title"], fontSize=22, leading=28)
subtitle = ParagraphStyle("sub", parent=title, fontSize=14, leading=19)
h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=15, spaceBefore=14, spaceAfter=6, textColor=colors.HexColor("#1F3864"))
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=12.5, spaceBefore=10, spaceAfter=4)
body = ParagraphStyle("body", parent=styles["BodyText"], fontSize=11, leading=15.5, alignment=TA_JUSTIFY, spaceAfter=6)
bullet = ParagraphStyle("bullet", parent=body, alignment=0, leftIndent=14, spaceAfter=3)
center = ParagraphStyle("center", parent=body, alignment=TA_CENTER)
mono = ParagraphStyle("mono", parent=styles["Code"], fontSize=9.5, leading=13, leftIndent=10, spaceAfter=6)

def P(t, s=body): return Paragraph(t, s)
def bullets(items): return [P(f"- {i}", bullet) for i in items]
def make_table(rows, widths):
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1F3864")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),0.5,colors.grey),("FONTSIZE",(0,0),(-1,-1),10.5),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
    return t

story = []
story.append(Spacer(1, 3*cm))
story.append(P("PROJECT REPORT", title)); story.append(Spacer(1, 0.5*cm))
story.append(P("Automated Web Scraping &amp; CRM Data Synchronization", subtitle))
story.append(Spacer(1, 1.2*cm))
story.append(P("Submitted by: <b>Aditya Mishra</b>", center))
story.append(P("BCA Student, Lovely Professional University (Expected 2027)", center))
story.append(P("Date: 11 November 2026", center)); story.append(Spacer(1, 1*cm))
story.append(P("GitHub Repository: https://github.com/Adi-dot0/automated-web-scraping-crm-sync", center))
story.append(PageBreak())

story.append(P("1. Abstract", h1))
story.append(P("This project automates the collection of product data from a website and its synchronization with a CRM system. A Python scraper collects records page by page from books.toscrape.com, a public website built specifically for scraping practice. The data is validated and formatted (price parsing, rating conversion, duplicate removal), stored in a database, and prepared for synchronization to HubSpot CRM as products, with a duplicate check before creating any record. A Streamlit dashboard monitors scraping and sync status. In the verified live run, the system scraped 60 real records, stored all 60, and on a second run created 0 duplicates - all 60 records were correctly recognized as updates."))

story.append(P("2. Business Problem", h1))
story.append(P("Businesses collect product information, pricing updates and competitor data from websites manually. Manual collection wastes time and produces outdated, inconsistent data. Automating collection, validation and CRM synchronization keeps business data updated without repeated manual work."))

story.append(P("3. Objectives", h1))
story.extend(bullets([
    "Collect structured data from website pages automatically, including pagination",
    "Validate and format scraped data and remove duplicate records",
    "Store scraped data in a structured database with sync history",
    "Synchronize validated records with HubSpot CRM without creating duplicates",
    "Monitor scraping status, CRM sync status and data quality in a dashboard",
    "Follow responsible scraping practice: permitted target site, polite request rate, self-identifying user agent",
]))

story.append(P("4. Technology Stack", h1))
story.append(make_table([
    ["Tool", "Use in this project"],
    ["Python", "Automation and pipeline logic"],
    ["Requests + BeautifulSoup", "Web scraping of HTML pages"],
    ["Selenium", "Ready module for JavaScript-heavy websites (not needed for the demo site)"],
    ["Pandas", "Data handling and CSV exports"],
    ["SQLite", "Storage of scraped records, sync history and duplicate log"],
    ["HubSpot API", "CRM synchronization (products), live mode with a private-app token"],
    ["Streamlit", "Monitoring dashboard"],
    ["GitHub", "Version control and project hosting"],
], [4.5*cm, 10.5*cm]))

story.append(P("5. System Architecture", h1))
story.append(P("Website Pages &rarr; Scraper (Requests + BeautifulSoup) &rarr; Validation and Formatting &rarr; Deduplication &rarr; Database Storage &rarr; CRM Synchronization (HubSpot) &rarr; Monitoring Dashboard (Streamlit)", ParagraphStyle("flow", parent=body, alignment=TA_CENTER)))

story.append(P("6. Modules of the System", h1))
story.append(P("Module 1 - Website Scraping (scrapers/)", h2))
story.append(P("website_scraper.py sends requests with a self-identifying user agent, follows the catalogue pagination (page-1, page-2, ...), waits one second between pages, and parses each product card into a raw record: title, price text, rating, availability and product URL. selenium_handler.py provides the browser-automation pattern for websites that load data with JavaScript."))
story.append(P("Module 2 - Data Validation and Formatting (processing/data_validation.py)", h2))
story.append(P("Prices are parsed from text such as a pound amount into numbers, star ratings given as words (One to Five) become numbers 1 to 5, availability is standardized to In stock or Out of stock, and records missing a title, price or URL are rejected. Duplicates are detected by product URL, which is the unique key of a record."))
story.append(P("Module 3 - Database Storage (database/)", h2))
story.append(P("Three tables: scraped_records (one row per product, product_url unique), sync_history (every sync run with counts and status) and duplicate_log. Storing uses the unique key: a new URL is inserted, an existing URL is updated with the latest price and rating, so re-scraping never creates duplicates."))
story.append(P("Module 4 - CRM Synchronization (crm/)", h2))
story.append(P("hubspot_api.py maps each record to a HubSpot Product (name, price, and a description containing rating, availability and the source URL) and searches HubSpot by source URL before creating, so records are updated rather than duplicated. crm_sync.py runs in two modes: live mode when a HubSpot private-app token is provided through an environment variable, and dry-run mode by default, in which no data leaves the machine and a hubspot_import.csv file is produced for manual import. Both modes are recorded in sync_history."))
story.append(P("Module 5 - Monitoring Dashboard (dashboard/app.py)", h2))
story.append(P("A Streamlit dashboard reads the database and shows total records, sync runs and last sync status, duplicates logged, the rating distribution, a price summary, and the full record and sync-history tables."))

story.append(P("7. How to Run the Project", h1))
story.append(P("pip install -r requirements.txt", mono))
story.append(P("python main.py", mono))
story.append(P("streamlit run dashboard/app.py   (monitoring dashboard)", mono))
story.append(P("For live HubSpot sync, set the environment variable HUBSPOT_ACCESS_TOKEN to a private-app token from your own free HubSpot account, then run main.py again. The token is never stored in the code.", body))

story.append(P("8. Testing and Results", h1))
story.append(P("Unit tests", h2))
story.append(P("Six unit tests cover: parsing a saved HTML page fixture (3 products, correct fields), price cleaning, validation with planted duplicate and invalid rows, the HubSpot payload mapping, and database insert-then-update behaviour. Tests run offline. All 6 tests pass."))
story.append(P("Live run results (11 November 2026)", h2))
story.append(P("The pipeline was run live against books.toscrape.com, a website created for scraping practice, collecting pages 1 to 3:", body))
story.append(make_table([
    ["Measure", "Result"],
    ["Records scraped (3 pages)", "60"],
    ["Valid after validation", "60 (0 invalid, 0 duplicates - site data is clean)"],
    ["Stored in database (run 1)", "60 new"],
    ["Second run", "0 new, 60 updated - no duplicates created"],
    ["CRM sync", "DryRun mode: 60 records prepared, hubspot_import.csv written"],
    ["Ratings distribution", "1 star: 15, 2 star: 8, 3 star: 13, 4 star: 10, 5 star: 14"],
    ["Price range (GBP)", "12.84 to 57.31, average 35.00"],
    ["Example record", "A Light in the Attic - GBP 51.77 - rating 3"],
], [6*cm, 9*cm]))
story.append(P("The second run is the important verification: a synchronization system that cannot recognize existing records would double the database and the CRM. Here the unique-key check worked live - 60 updates, 0 duplicates, and both runs appear in sync_history.", body))

story.append(P("9. Responsible Scraping", h1))
story.append(P("The target website is a sandbox created for scraping practice. The scraper identifies itself in its user agent, waits between page requests, and collects only public product listing data, not personal data. For any real website, the same checks apply first: read the site's terms and robots rules and scrape only what is permitted.", body))

story.append(P("10. Limitations", h1))
story.extend(bullets([
    "Live HubSpot synchronization requires the user's own free HubSpot account and private-app token; the verified runs used dry-run mode, in which nothing is sent to HubSpot",
    "The Selenium module is provided for JavaScript-heavy sites but is not exercised by the demo site, which is plain HTML",
    "The parser is written for the demo site's page structure; another website needs its selectors updated",
    "Prices are in GBP because the demo site prices in pounds",
]))

story.append(P("11. Future Scope", h1))
story.append(P("Connect a live HubSpot account and verify create/update against the real API; add scheduling so scraping runs daily; extend the scraper to a second permitted source; and add the dashboard to the deployed portfolio alongside Projects 1 and 2.", body))

story.append(P("12. Conclusion", h1))
story.append(P("The system completes the full path from public web pages to CRM-ready data: automated collection with pagination, validation and formatting, duplicate-safe database storage, HubSpot synchronization with duplicate checking in both dry-run and live modes, and a monitoring dashboard. Live verification on a real (practice) website showed 60 records collected and stored, and a second run that updated all 60 without creating a single duplicate. The complete project is available on GitHub at https://github.com/Adi-dot0/automated-web-scraping-crm-sync", body))

story.append(P("Appendix - Project Files", h1))
story.append(P("main.py; scrapers/website_scraper.py and selenium_handler.py; processing/data_validation.py; database/schema.sql and db.py; crm/hubspot_api.py and crm_sync.py; dashboard/app.py; config/config.json; reports/scraped_products.csv and hubspot_import.csv; tests (3 test files + HTML fixture); requirements.txt; README.md.", body))

doc = SimpleDocTemplate(OUT, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm, leftMargin=2*cm, rightMargin=2*cm,
                        title="Project Report - Automated Web Scraping & CRM Synchronization", author="Aditya Mishra")
doc.build(story)
print("built", OUT)
