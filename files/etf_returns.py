import yfinance as yf
import pandas as pd

tickers = ["SPY", "GLD", "UUP", "IEF", "EFA"]

prices = yf.download(tickers, start="1990-01-01", auto_adjust=True)["Close"]

# End-of-month prices
prices = prices.resample("ME").last()

# Monthly returns
returns = prices.pct_change()

# Drop NaN rows and March 2026
returns = returns.dropna()
returns = returns[~((returns.index.year == 2026) & (returns.index.month == 3))]

print(returns.shape)
print(returns.head())
print(returns.tail())

returns.to_excel("ETF-returns.xlsx")
print("Saved to ETF-returns.xlsx")
