import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Parameters
ticker = 'SNEX'  # Stock ticker
start = '2021-01-01'
end = '2024-01-01'
k_period = [7, 14, 21, 28, 35, 42, 49, 56]  # Lookback period for %K
d_period = 3  # Lookback period for %D (moving average of %K)
overbought = 80  # Overbought level
oversold = 20  # Oversold level
initial_cash = 10000  # Starting cash
portfolio_allocation = 0.5  # Full allocation

asset_data = yf.Ticker(ticker)
asset_data = asset_data.history(start=start, end=end)
profit_run = []

for k in k_period:
    # Calculate Stochastic Oscillator %K and %D
    asset_data['Lowest Low'] = asset_data['Low'].rolling(window=k).min()
    asset_data['Highest High'] = asset_data['High'].rolling(window=k).max()
    asset_data['%K'] = 100 * ((asset_data['Close'] - asset_data['Lowest Low']) / (asset_data['Highest High'] - asset_data['Lowest Low']))
    asset_data['%D'] = asset_data['%K'].rolling(window=d_period).mean()

    asset_data = asset_data.iloc[k:]

    # Initialize variables for the trading algorithm
    cash = initial_cash
    position = 0
    equity = initial_cash
    cash_run = []
    cash_run.append(cash)
    equity_run = []
    equity_run.append(equity)

    # Trading Algorithm
    for i in range(1, len(asset_data)):
        price = asset_data['Close'].iloc[i]
        prev_k = asset_data['%K'].iloc[i - 1]
        curr_k = asset_data['%K'].iloc[i]
        curr_d = asset_data['%D'].iloc[i]

        # Buy Signal: %K crosses above %D and %K is below the oversold level
        if curr_k > curr_d and prev_k <= curr_d and curr_k < oversold and cash > 0:
            position += portfolio_allocation * cash / price
            cash -= portfolio_allocation * cash
            print(f"Buying at {price:.2f} on {asset_data.index[i].date()}")

        # Sell Signal: %K crosses below %D and %K is above the overbought level
        elif curr_k < curr_d and prev_k >= curr_d and curr_k > overbought and position > 0:
            position -= portfolio_allocation * cash / price
            cash += portfolio_allocation * cash
            print(f"Selling at {price:.2f} on {asset_data.index[i].date()}")

        # Update cash and equity
        cash_run.append(cash)
        equity = cash + position * price
        equity_run.append(equity)

    # Add equity to the DataFrame for plotting
    asset_data['Equity'] = equity_run

    profit = round(asset_data['Equity'].iloc[-1] - initial_cash, 1)
    profit_run.append(profit)

    # Plot the results
    plt.figure(figsize=(12, 8))

    # Plot %K and %D
    plt.subplot(3, 1, 1)
    plt.plot(asset_data['%K'], label='%K')
    plt.plot(asset_data['%D'], label='%D')
    plt.axhline(y=overbought, color='r', linestyle='--', label='Overbought')
    plt.axhline(y=oversold, color='g', linestyle='--', label='Oversold')
    plt.title(f'{ticker} Stochastic Oscillator')
    plt.legend()

    # Plot the stock price
    plt.subplot(3, 1, 2)
    plt.plot(asset_data['Close'], label='Close Price')
    plt.title(f'{ticker} Stock Price')
    plt.legend()

    # Plot the equity curve
    plt.subplot(3, 1, 3)
    plt.plot(asset_data['Equity'], label='Equity')
    plt.title('Equity Curve')
    plt.legend()

    plt.suptitle(f'Financial Analysis: {ticker}, Profit: £{profit}, K period ={k}', fontsize=16)

    plt.tight_layout()

print(f'Optimum k period is {k_period[profit_run.index(max(profit_run))]} days')

plt.figure()
plt.plot(k_period, profit_run, label='%K')
plt.title('Profit vs k period')
plt.show()