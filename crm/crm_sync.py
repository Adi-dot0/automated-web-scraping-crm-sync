import csv
import os

from database.db import log_sync

BASE = os.path.dirname(os.path.dirname(__file__))


def sync_records(records, new_count, updated_count):
    """Sync validated records to HubSpot.

    Two modes:
    - LIVE: when the environment variable HUBSPOT_ACCESS_TOKEN is set,
      records are created/updated in HubSpot through crm/hubspot_api.py
      (duplicate check by source URL before creating).
    - DRY-RUN (default, no token): no data leaves the machine. The exact
      HubSpot payloads are counted as ready and a hubspot_import.csv is
      written, which can be imported into HubSpot manually
      (CRM -> Products -> Import).
    """
    token = os.environ.get("HUBSPOT_ACCESS_TOKEN", "")

    if token:
        from crm.hubspot_api import find_product_by_source_url, create_product, update_product
        created, updated, errors = 0, 0, []
        for r in records:
            try:
                existing_id = find_product_by_source_url(r["product_url"])
                if existing_id:
                    update_product(existing_id, r)
                    updated += 1
                else:
                    create_product(r)
                    created += 1
            except Exception as e:
                errors.append(f"{r['title']}: {e}")
        status = "Live" if not errors else "LiveWithErrors"
        log_sync(created + updated, created, updated, status, "; ".join(errors[:3]))
        return {"mode": "live", "created": created, "updated": updated, "errors": len(errors)}

    # dry-run mode
    export_path = os.path.join(BASE, "reports", "hubspot_import.csv")
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    with open(export_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Price", "Description", "Source URL"])
        for r in records:
            writer.writerow([
                r["title"], r["price"],
                f"Rating: {r['rating']}/5 | Availability: {r['availability']}",
                r["product_url"],
            ])
    log_sync(len(records), new_count, updated_count, "DryRun")
    return {"mode": "dry-run", "records_ready": len(records), "export_file": export_path}
