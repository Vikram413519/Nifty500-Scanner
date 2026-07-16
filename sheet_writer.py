from sheet import connect_sheet
from config import SCANNER_SHEET


def write_to_scanner(data):

    sheet = connect_sheet(SCANNER_SHEET)

    # पुराना data clear
    sheet.clear()

    # Header
    header = [
        "Stock",
        "Price",
        "EMA20",
        "EMA50",
        "RSI",
        "Signal"
    ]

    sheet.update("A1", [header])

    # Data write
    if data:
        sheet.update(
            "A2",
            data
        )

    print("Scanner Sheet Updated Successfully")
