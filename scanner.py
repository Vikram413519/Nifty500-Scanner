# ==============================
# NIFTY 500 SWING SCANNER
# scanner.py
# ==============================

from datetime import datetime
import yfinance as yf
import pandas as pd
import time

from indicators import calculate_indicators, generate_signal
from sheet import (
    get_sheet_data,
    write_results,
    write_sorted_data
)
from telegram_alert import send_telegram

# ==============================
# SETTINGS
# ==============================

TIMEFRAME = "1d"
PERIOD = "2y"


# ==============================
# STOCK PROCESS
# ==============================

def scan_stock(symbol):

    try:

        print("Processing :", symbol)

        df = yf.download(
            symbol + ".NS",
            period=PERIOD,
            interval=TIMEFRAME,
            progress=False
        )

        if df.empty:
            return None

        # Reset Date Index
        df.reset_index(inplace=True)

        # Indicators
        df = calculate_indicators(df)

        # Latest Candle
        last = df.iloc[-1]

        # Signal
        signal, score, setup = generate_signal(last)

        # Trade Levels
        price = round(float(last["Close"]), 2)
        atr = round(float(last["ATR"]), 2)

        entry = price
        stop_loss = round(price - atr, 2)
        target = round(price + (atr * 2), 2)

        supertrend = "Bullish" if last["Supertrend"] == 1 else "Bearish"
        breakout = "YES" if price >= float(last["High20"]) else "NO"

        result = {
            "Stock": symbol,
            "Price": price,
            "EMA20": round(float(last["EMA20"]), 2),
            "EMA50": round(float(last["EMA50"]), 2),
            "EMA200": round(float(last["EMA200"]), 2),
            "RSI": round(float(last["RSI"]), 2),
            "ATR": atr,
            "Supertrend": supertrend,
            "Volume": int(last["Volume"]),
            "Breakout": breakout,
            "Entry": entry,
            "Stop Loss": stop_loss,
            "Target": target,
            "Score": score,
            "Signal": signal,
            "Trade Setup": setup
        }

        return result

    except Exception as e:

        print(symbol, "Error :", e)

        return None
# ==============================
# MAIN
# ==============================

def main():

    print("\nStarting Nifty500 Scanner\n")

    stocks = get_sheet_data()

    print("Total Stocks :", len(stocks))

    results = []

    for stock in stocks:

        data = scan_stock(stock)

        if data:
            results.append(data)

        time.sleep(1)

    if results:

        df = pd.DataFrame(results)

        df = df.sort_values(
            by="Score",
            ascending=False
        )

        write_results(df)

        write_sorted_data(df)

        # ==========================
        # TELEGRAM SUMMARY
        # ==========================

        strong_buy = df[df["Signal"] == "STRONG BUY"]
        buy = df[df["Signal"] == "BUY"]

        message = f"""📈 <b>NIFTY 500 SWING SCANNER</b>

📅 {datetime.now().strftime("%d-%b-%Y")}
🕒 {datetime.now().strftime("%I:%M %p")}

"""

        if not strong_buy.empty:

            message += f"🟢 <b>STRONG BUY ({len(strong_buy)})</b>\n\n"

            for _, row in strong_buy.iterrows():

                message += (
                    f"• <b>{row['Stock']}</b>\n"
                    f"Price : ₹{row['Price']}\n"
                    f"Score : {row['Score']}\n\n"
                )

        if not buy.empty:

            message += f"\n🔵 <b>BUY ({len(buy)})</b>\n\n"

            for _, row in buy.iterrows():

                message += (
                    f"• <b>{row['Stock']}</b>\n"
                    f"Price : ₹{row['Price']}\n"
                    f"Score : {row['Score']}\n\n"
                )

        message += f"\n━━━━━━━━━━━━━━\nTotal Signals : {len(strong_buy) + len(buy)}"

        if len(strong_buy) + len(buy) > 0:
            send_telegram(message)

        print("\nScanner Completed")

    else:

        print("No Data Found")


if __name__ == "__main__":
    main()
