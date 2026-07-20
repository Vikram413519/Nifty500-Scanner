import os
from flask import Flask, render_template
from sheet import get_scanner_data

app = Flask(__name__)


@app.route("/")
def home():

    # Read Scanner Data
    df = get_scanner_data()

    # Total Counts
    strong_buy = len(df[df["Signal"] == "STRONG BUY"])
    buy = len(df[df["Signal"] == "BUY"])
    watch = len(df[df["Signal"] == "WATCH"])
    avoid = len(df[df["Signal"] == "AVOID"])

    # Top 50 Rows
    table = df.to_dict(orient="records")

    return render_template(
        "index.html",
        strong_buy=strong_buy,
        buy=buy,
        watch=watch,
        avoid=avoid,
        table=table
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
