# ==============================
# GOOGLE SHEET CONNECTOR
# sheet.py
# ==============================

import os
import json
import tempfile

import gspread
import pandas as pd

from oauth2client.service_account import ServiceAccountCredentials

from config import (
    GOOGLE_SHEET_NAME,
    STOCK_LIST_SHEET,
    SCANNER_SHEET,
    SORTED_SHEET
)

# ==============================
# CONNECT GOOGLE SHEET
# ==============================

def connect_sheet(sheet_name):

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    # ==========================
    # GitHub Actions
    # ==========================
    if os.getenv("GOOGLE_CREDENTIALS"):

        credentials = json.loads(os.environ["GOOGLE_CREDENTIALS"])

        with tempfile.NamedTemporaryFile(
            mode="w",
            delete=False,
            suffix=".json"
        ) as f:

            json.dump(credentials, f)
            temp_file = f.name

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            temp_file,
            scope
        )

    # ==========================
    # Local PC
    # ==========================
    else:

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials.json",
            scope
        )

    client = gspread.authorize(creds)

    spreadsheet = client.open(GOOGLE_SHEET_NAME)

    print("Connected :", spreadsheet.title)

    return spreadsheet.worksheet(sheet_name)

# ==============================
# READ STOCK LIST
# ==============================

def get_sheet_data():

    sheet = connect_sheet(STOCK_LIST_SHEET)

    data = sheet.col_values(1)

    stocks = []

    for stock in data[1:]:

        stock = stock.strip().upper()

        if stock:
            stocks.append(stock)

    return stocks

# ==============================
# WRITE SCANNER RESULT
# ==============================

def write_results(df):

    sheet = connect_sheet(SCANNER_SHEET)

    df = df.fillna("")

    data = [df.columns.tolist()] + df.astype(str).values.tolist()

    sheet.clear()

    sheet.update("A1", data)

    print("Scanner Sheet Updated")

# ==============================
# WRITE SORTED DATA
# ==============================

def write_sorted_data(df):

    sheet = connect_sheet(SORTED_SHEET)

    buy_df = df[
        (df["Signal"] == "BUY") |
        (df["Signal"] == "STRONG BUY")
    ]

    buy_df = buy_df.sort_values(
        by="Score",
        ascending=False
    )

    buy_df = buy_df.fillna("")

    data = [buy_df.columns.tolist()] + buy_df.astype(str).values.tolist()

    sheet.clear()

    sheet.update("A1", data)

    print("Sorted Sheet Updated")
