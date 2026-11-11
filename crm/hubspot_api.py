import os
import requests

# HubSpot CRM API (v3) integration.
# The access token is read from the environment variable
# HUBSPOT_ACCESS_TOKEN - never write a token in the code or in git.
# In HubSpot: Settings -> Integrations -> Private Apps -> create an app
# with the crm.objects.products read/write scopes to get a token.
#
# Records are synced as HubSpot Products (name, price, description).
# The product URL from the source website is used as the unique key:
# before creating, the code searches HubSpot for that description URL,
# so the same record is updated, not duplicated.

BASE_URL = "https://api.hubapi.com/crm/v3/objects/products"


def _headers():
    token = os.environ.get("HUBSPOT_ACCESS_TOKEN", "")
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def record_to_hubspot_properties(record):
    return {
        "name": record["title"],
        "price": str(record["price"]),
        "description": f"Rating: {record['rating']}/5 | Availability: {record['availability']} | Source: {record['product_url']}",
    }


def find_product_by_source_url(product_url):
    """Search HubSpot for a product whose description contains the source URL."""
    url = "https://api.hubapi.com/crm/v3/objects/products/search"
    body = {
        "filterGroups": [{
            "filters": [{"propertyName": "description", "operator": "CONTAINS_TOKEN", "value": product_url.split("/")[-2]}]
        }],
        "properties": ["name", "description"],
        "limit": 5,
    }
    response = requests.post(url, headers=_headers(), json=body, timeout=20)
    response.raise_for_status()
    results = response.json().get("results", [])
    for item in results:
        if product_url in item.get("properties", {}).get("description", ""):
            return item["id"]
    return None


def create_product(record):
    response = requests.post(BASE_URL, headers=_headers(),
                             json={"properties": record_to_hubspot_properties(record)}, timeout=20)
    response.raise_for_status()
    return response.json().get("id")


def update_product(hubspot_id, record):
    url = f"{BASE_URL}/{hubspot_id}"
    response = requests.patch(url, headers=_headers(),
                              json={"properties": record_to_hubspot_properties(record)}, timeout=20)
    response.raise_for_status()
    return hubspot_id
