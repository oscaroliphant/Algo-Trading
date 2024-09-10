import datetime as dt
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

ticker = 'SNEX'
start = dt.datetime.now() - dt.timedelta(days=365*2)
end = dt.datetime.now()
asset_data = yf.Ticker(ticker)
asset_data = asset_data.history(start=start, end=end)

x = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
profit_run = []

for dt in x:
    cash_0 = 1000
    cash = 1000
    position = 0  # number of shares
    portfolio_allocation = 0.5  # fraction of cash allocated to buying shares

    cash_run = []
    cash_run.append(cash)
    position_run = []
    position_run.append(position)
    equity_run = []
    equity_run.append(cash)

    asset_data['Max High'] = asset_data['High'].rolling(window=dt).max()
    asset_data['Min Low'] = asset_data['Low'].rolling(window=dt).min()
    asset_data = asset_data.iloc[dt:]

    for i in range(1, len(asset_data)):
        price = asset_data['Close'].iloc[i]
        levels = [asset_data['Max High'].iloc[i] - (asset_data['Max High'].iloc[i] - asset_data['Min Low'].iloc[i]) * ratio for ratio in [0.236, 0.382, 0.5, 0.618, 1]]
        buy_threshold = levels[2]  # Buy at the 50% retracement level
        sell_threshold = levels[1]  # Sell at the 38.2% retracement level

        if price < buy_threshold and asset_data['Close'].iloc[i - 1] >= buy_threshold and cash_run[i - 1] > 0:
            position = position_run[i - 1] + portfolio_allocation * cash_run[i - 1] / price
            cash = cash_run[i - 1] - portfolio_allocation * cash_run[i - 1]
            print(f"Buying at {price} on {asset_data.index[i].date()}")
        elif price > sell_threshold and asset_data['Close'].iloc[i - 1] <= sell_threshold and position_run[i - 1] > 0:
            position = position_run[i - 1] - portfolio_allocation * cash_run[i - 1] / price
            cash = cash_run[i - 1] + portfolio_allocation * position_run[i - 1] * price
            print(f"Selling at {price} on {asset_data.index[i].date()}")
        else:
            # Carry forward the previous values if no trade is made
            position = position_run[i - 1]
            cash = cash_run[i - 1]

        position_run.append(position)  # Append the updated position
        cash_run.append(cash)  # Append the updated cash
        equity_run.append(cash + position * price)  # Append the updated equity

    asset_data['Equity'] = equity_run
    asset_data['Cash'] = cash_run
    asset_data['Position'] = position_run

    profit = round(asset_data['Equity'].iloc[-1] - cash_0, 1)
    profit_run.append(profit)

    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
    axs[0].plot(asset_data['Equity'], label='Equity')
    axs[0].plot(asset_data['Cash'], label='Cash')
    axs[0].set_xlabel('Date')  # Set x-axis label for the first subplot
    axs[0].set_ylabel('Value')  # Set y-axis label for the first subplot
    axs[0].legend()

    axs[1].plot(asset_data['Close'], label='Close Price')
    axs[1].set_xlabel('Date')  # Set x-axis label for the second subplot
    axs[1].set_ylabel('Value')  # Set y-axis label for the second subplot
    axs[1].legend()

    fig.suptitle(f'Financial Analysis: {ticker}, Profit: £{profit}, dt={dt}', fontsize=16)

plt.figure()
plt.plot(x, profit_run)
plt.show()

print('test')