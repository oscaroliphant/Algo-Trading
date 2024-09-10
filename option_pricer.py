import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from scipy.stats import norm

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

ticker = 'SNEX'
start = datetime.now() - timedelta(days=365)
end = datetime.now()
data = yf.download(ticker, start=start, end=end)

def black_scholes(S, K, T, r, sigma, option_type):

    # Calculate d1 and d2 using the Black-Scholes formula
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        # Call option price formula
        call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        return call_price
    elif option_type == "put":
        # Put option price formula
        put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return put_price
    else:
        raise ValueError("Invalid option_type. Must be 'call' or 'put'.")


# Example usage:
S = data['Close'].iloc[-1]  # Spot price
K = S*np.arange(0.5, 1.5, 0.1) # Strike prices
T = 1  # Time to maturity in years
r = 0.05  # Risk-free interest rate (5%)
sigma = 0.2  # Volatility (20%)
call_price = []
put_price = []
spot = []

for i in K:
    call_price.append(black_scholes(S, i, T, r, sigma, option_type="call"))
    put_price.append(black_scholes(S, i, T, r, sigma, option_type="put"))
    spot.append(S)

df = pd.DataFrame({f'Last Close Since {str(end).split()[0]}':spot, 'Call Price':call_price, 'Put Price':put_price, 'Strike':K})
print(df)
