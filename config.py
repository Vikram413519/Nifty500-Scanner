import os

# ===========================
# GOOGLE SHEET SETTINGS
# ===========================

GOOGLE_SHEET_NAME = "Top 250 Stocks"
STOCK_LIST_SHEET = "Stock List"
SCANNER_SHEET = "Nifty 500 Swing Scanner"
SORTED_SHEET = "sorted data"
SETTINGS_SHEET = "Settings"

# ===========================
# TELEGRAM SETTINGS
# ===========================

TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN",
    "8972849338:AAEuLHmevaTVusZ86OlkCLXtAC3WbbT-QCc"
)

TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    "6939885314"
)


