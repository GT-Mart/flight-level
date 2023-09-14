# -*- coding: utf-8 -*-
import sys
import duckdb
import pandas as pd
import json

from .log import get_logger

import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

logger = None


# Your SharePoint site details
def run(config, job_name):
    site_url = "https://gtmart234.sharepoint.com"
    list_name = "SalesData"

    # Your SharePoint App-Only credentials
    client_id = config.SHP_CLIENT_ID
    client_secret = config.SHP_CLIENT_SECRET
    tenant_id = "2b2830bc-03fb-4ea1-88c2-cb37161501be"
    resource = f"https://{tenant_id}.sharepoint.com/"

    token = config.SHP_TOKEN

    # Get all items from the SharePoint list
    headers = {
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/json;odata=verbose",
        "Authorization": f"Bearer {token}",
    }
    items_url = f"{site_url}/_api/web/lists/getbytitle('{list_name}')/items"
    items_r = requests.get(items_url, headers=headers)
    items = items_r.json()["d"]["results"]

    # Delete all items from the SharePoint list
    for item in items:
        print(item)
        # delete_url = (
        #     f"{site_url}/_api/web/lists/getbytitle('{list_name}')/items({item['ID']})"
        # )
        # delete_headers = headers.copy()
        # delete_headers["IF-MATCH"] = "*"
        # delete_r = requests.delete(delete_url, headers=delete_headers)

    # Read the CSV file and add each row as a new item in the SharePoint list
    data = pd.read_csv("data/all_sales.csv")
    for index, row in data.iterrows():
        add_url = f"{site_url}/_api/web/lists/getbytitle('{list_name}')/items"
        add_data = {
            "__metadata": {
                "type": "SP.Data.SalesDataListItem"
            },  # Replace SalesDataListItem with the correct ListItemEntityTypeFullName for your list
            # product_id,product_name,product_category,package_qty,sales_qty,product_price,sales_price,category_pct,day_pct,sales_date
            "Title": str(row["product_id"]),
            "product_name": row["product_name"],
            "product_category": row["product_category"],
            "package_qty": row["package_qty"],
            "sales_qty": row["sales_qty"],
            "product_price": row["product_price"],
            "sales_price": row["sales_price"],
            "category_pct": row["category_pct"],
            "day_pct": row["day_pct"],
            "sales_date": row["sales_date"],
        }
        add_r = requests.post(add_url, json=add_data, headers=headers)
        print(add_r.json())

        if index % 2 == 0:
            break
