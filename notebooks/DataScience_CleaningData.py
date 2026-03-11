import time
import yfinance as yf
import pandas as pd
import numpy as np

TICKERS = ["XLF","XLC","XLE","XLB","XLI", "XLK","XLP","XLRE","XLU","XLV","XLY"]

START_DATE = "2000-01-01"

all_prices = []

for ticker in TICKERS:
    df = yf.download(ticker, start=START_DATE, progress=False)["Adj Close"]
    df = df.rename(ticker)
    all_prices.append(df)
    time.sleep(1.5)

prices = pd.concat(all_prices, axis=1)

prices.index = pd.to_datetime(prices.index)
prices = prices.dropna(how="any")
prices = prices[~prices.index.duplicated()]

log_returns = np.log(prices).diff().dropna()
prices.to_csv("sector_prices.csv")
log_returns.to_csv("sector_log_returns.csv")

print("Saved:")
print(" - sector_prices.csv")
print(" - sector_log_returns.csv")
print("\nDate range:", prices.index.min().date(), "to", prices.index.max().date())
print("Observations:", prices.shape[0])
