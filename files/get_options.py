"""
Fetch options market data from Yahoo Finance.

This script pulls 15-minute delayed options data from the CBOE
(Chicago Board Options Exchange) via Yahoo Finance.

Usage:
    from get_options import get_options_data
    data = get_options_data("AAPL", weeks_out=4)
"""

import subprocess
import sys

# Ensure required libraries are installed
for pkg in ["yfinance", "pandas"]:
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def get_options_data(ticker: str, weeks_out: int = 4, option_type: str = "call"):
    """
    Fetch options chain data for a given ticker and approximate maturity.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol (e.g., "AAPL").
    weeks_out : int
        Approximate number of weeks until expiration. The function selects
        the available expiration date closest to this target.
    option_type : str
        "call" or "put".

    Returns
    -------
    dict with keys:
        "chain" : pd.DataFrame
            Options data with columns: Strike, Bid, Ask, Mid, Last Price,
            Volume, Open Interest.
        "expiration" : str
            The selected expiration date (YYYY-MM-DD).
        "stock_price" : float
            Last traded stock price.
    """
    tick = yf.Ticker(ticker.upper())

    # Get last stock price
    stock_price = tick.history().iloc[-1].Close

    # Find the expiration date closest to the target
    target_date = datetime.today() + timedelta(weeks=weeks_out)
    expirations = tick.options  # list of date strings
    best = min(expirations, key=lambda d: abs(datetime.strptime(d, "%Y-%m-%d") - target_date))

    # Pull options chain
    chain = tick.option_chain(best)
    df = chain.calls if option_type == "call" else chain.puts

    # Select and rename columns
    df = df[["strike", "bid", "ask", "lastPrice", "volume", "openInterest"]].copy()
    df.columns = ["Strike", "Bid", "Ask", "Last Price", "Volume", "Open Interest"]
    df["Mid"] = (df["Bid"] + df["Ask"]) / 2

    # Reorder so Mid is after Ask
    df = df[["Strike", "Bid", "Ask", "Mid", "Last Price", "Volume", "Open Interest"]]

    return {
        "chain": df,
        "expiration": best,
        "stock_price": stock_price,
    }
