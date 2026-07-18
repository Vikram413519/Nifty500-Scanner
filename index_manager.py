# ==============================
# INDEX MANAGER
# Automatically updates Stock List
# ==============================

import requests
import pandas as pd
from io import StringIO

from sheet import connect_sheet, get_selected_index
from config import STOCK_LIST_SHEET

# ==============================
# NSE INDEX URLS
# ==============================

INDEX_URLS = {

    "NIFTY500":
    "https://archives.nseindia.com/content/indices/ind_nifty500list.csv",

}

# ==============================
# UPDATE STOCK LIST
# ==============================

def update_stock_list():

    index_name = get_selected_index()

    if index_name not in INDEX_URLS:
        print(f"Index not supported : {index_name}")
        return

    print(f"Downloading {index_name}...")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        INDEX_URLS[index_name],
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    df = pd.read_csv(
        StringIO(response.text)
    )

    symbols = (
        df["Symbol"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    sheet = connect_sheet(STOCK_LIST_SHEET)

    sheet.clear()

    data = [["Symbol"]]

    for symbol in symbols:
        data.append([symbol])

    sheet.update("A1", data)

    print(f"{len(symbols)} Stocks Updated")


# ==============================

if __name__ == "__main__":

    update_stock_list()
