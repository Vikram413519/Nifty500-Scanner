import ta
import pandas as pd


def calculate_indicators(df):

    # Fix yfinance Multi Index
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)


    # Convert numeric

    for col in ["Open","High","Low","Close","Volume"]:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


    # =====================
    # EMA
    # =====================

    df["EMA20"] = ta.trend.ema_indicator(
        df["Close"],
        window=20
    )

    df["EMA50"] = ta.trend.ema_indicator(
        df["Close"],
        window=50
    )


    df["EMA200"] = ta.trend.ema_indicator(
        df["Close"],
        window=200
    )


    # =====================
    # RSI
    # =====================

    df["RSI"] = ta.momentum.rsi(
        df["Close"],
        window=14
    )


    # =====================
    # ATR
    # =====================

    df["ATR"] = ta.volatility.average_true_range(
        df["High"],
        df["Low"],
        df["Close"],
        window=14
    )


    # =====================
    # Supertrend Logic
    # =====================

    df["ST_Value"] = (
        df["Close"] -
        (3 * df["ATR"])
    )


    df["Supertrend"] = 0


    df.loc[
        df["Close"] > df["ST_Value"],
        "Supertrend"
    ] = 1


    df.loc[
        df["Close"] <= df["ST_Value"],
        "Supertrend"
    ] = -1



    # =====================
    # Volume
    # =====================

    df["AvgVolume"] = (
        df["Volume"]
        .rolling(20)
        .mean()
    )


    # =====================
    # Breakout
    # =====================

    df["High20"] = (
        df["High"]
        .rolling(20)
        .max()
    )


    return df



# =================================
# Signal Generator
# =================================

def generate_signal(row):

    price = float(row["Close"])

    ema20 = float(row["EMA20"])

    ema50 = float(row["EMA50"])

    ema200 = float(row["EMA200"])

    rsi = float(row["RSI"])

    score = 0


    # Trend

    if price > ema20 > ema50:

        score += 2

    elif price > ema20:

        score += 1



    # EMA200

    if price > ema200:

        score += 1



    # RSI

    if 55 <= rsi < 70:

        score += 1

    elif rsi >=70:

        score += 2



    # Supertrend

    if row["Supertrend"] == 1:

        score += 1



    # Volume

    if row["Volume"] > row["AvgVolume"]:

        score += 1



    # Breakout

    if price >= row["High20"]:

        score += 2



    # Final Signal

    if score >=7:

        signal = "STRONG BUY"

        setup = "Momentum Breakout"


    elif score >=5:

        signal = "BUY"

        setup = "Pullback Buy"


    elif score >=3:

        signal = "WATCH"

        setup = "Wait"


    else:

        signal = "AVOID"

        setup = "No Setup"



    return signal, score, setup
