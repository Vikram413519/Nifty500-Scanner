from sheet import connect_sheet

def get_stock_list():

    from config import STOCK_LIST_SHEET
    sheet = connect_sheet(STOCK_LIST_SHEET)

    values = sheet.col_values(1)

    stocks = []

    for stock in values[1:]:   # Header छोड़कर
        stock = stock.strip().upper()

        if stock:
            stocks.append(stock)

    return stocks
