# -*- coding: utf-8 -*-
import sys
import duckdb
import pandas as pd

from .log import get_logger

# from shareplum.site import Version
# from shareplum import Site, Office365
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext


logger = None


def authenticate(sp_url, sp_site, user_name, password):
    """
    Takes a SharePoint url, site url, username and password to access the SharePoint site.
    Returns a SharePoint Site instance if passing the authentication, returns None otherwise.
    """
    print(sp_url, sp_site, user_name, password)
    site = None
    try:
        authcookie = Office365(
            sp_url, username=user_name, password=password
        ).GetCookies()
        site = Site(
            sp_site, version=Version.v365, authcookie=authcookie, verify_ssl=False
        )
    except:
        # We should log the specific type of error occurred.
        print("Failed to connect to SP site: {}".format(sys.exc_info()[1]))
    return site


def run(config, job_name):
    global logger
    i = 0
    logger = get_logger(job_name, config)

    logger.info("Migrating data to sharepoint list...")

    logger.info("Connecting to the database...")
    con = duckdb.connect(config.DATABASE)

    client_credentials = ClientCredential(
        config.SHP_CLIENT_ID, config.SHP_CLIENT_SECRET
    )
    ctx = ClientContext(config.SHAREPOINT_URL).with_credentials(client_credentials)

    # sp_site = authenticate(
    #     config.SHAREPOINT_URL,
    #     config.SHAREPOINT_SITE,
    #     config.SHAREPOINT_USERNAME,
    #     config.SHAREPOINT_PASSWORD,
    # )

    # if sp_site is None:
    #     logger.info("falhou")

    web = ctx.web
    ctx.load(web)
    ctx.execute_query()

    if ctx:
        logger.info(f"Loading sales data...")
        df = con.query(
            """select  a.product_id, 
                    coalesce(p.product_name, a.product_name) as product_name,
                    coalesce(p.product_category, a.product_category) as product_category,
                    a.package_qty,
                    a.sales_qty,
                    a.product_price,
                    a.sales_price,
                    a.category_pct,
                    a.day_pct,
                    a.sales_date
            from all_sales a left join product p on a.product_id = p.product_id
          """
        ).to_df()
        logger.info(f" Size of the data: {df.shape}")
        logger.info(f"Saving data at: {config.PARQUET}")
        df.to_parquet(config.PARQUET)

        logger.info(f"Loading fuel data...")
        df2 = con.query(
            """select  *
            from all_fuel
          """
        ).to_df()
        logger.info(f" Size of the data: {df2.shape}")
        logger.info(f"Saving data at: {config.FUEL_PARQUET}")
        df2.to_parquet(config.FUEL_PARQUET)
        logger.info("Data dumped.")
    else:
        print("erro")
