def calculate_score(last, gap_percent, breakout, rr_ratio, weekly_trend):

    score = 0

    # Price above EMA20
    if last["Close"] > last["EMA20"]:
        score += 1

    # EMA20 above EMA50
    if last["EMA20"] > last["EMA50"]:
        score += 1

    # EMA50 above EMA200
    if last["EMA50"] > last["EMA200"]:
        score += 1

    # RSI
    if 55 <= last["RSI"] <= 70:
        score += 1

    # Supertrend
    if last["Close"] > last["Supertrend"]:
        score += 1

    # Volume Spike
    if last["Volume"] > last["Volume_Avg"] * 1.5:
        score += 1

    # Breakout
    if breakout == "YES":
        score += 1

    # Gap Up
    if 0.5 <= gap_percent <= 3:
        score += 1

    # Weekly Trend
    if weekly_trend == "Bullish":
        score += 1

    # Risk Reward
    if rr_ratio >= 2:
        score += 1

    return score