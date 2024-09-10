import datetime as dt
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import pandas_ta as ta

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

ma_1 = 30
ma_2 = 100

ticker = 'SNEX'
start = dt.datetime.now() - dt.timedelta(days=365*5)
end = dt.datetime.now()
asset_data = yf.Ticker(ticker)
asset_data = asset_data.history(start=start, end=end)
asset_data[f'SMA_{ma_1}'] = asset_data['Close'].rolling(window=ma_1).mean()
asset_data[f'SMA_{ma_2}'] = asset_data['Close'].rolling(window=ma_2).mean()

asset_data = asset_data.iloc[ma_2:]  # data from 100 days onwards
cash_0 = 1000
cash = 1000
position = 0  # number of shares
portfolio_allocation = 0.1  # fraction of cash allocated to buying shares

# Simple moving average crossover strategy:
cash_1 = []
cash_1.append(cash)
equity_1 = []
equity_1.append(cash)
for i in range(1, len(asset_data)):
    price = asset_data['Close'].iloc[i]
    if asset_data[f'SMA_{ma_1}'].iloc[i] >= asset_data[f'SMA_{ma_2}'][i] and asset_data[f'SMA_{ma_1}'].iloc[i-1] <= asset_data[f'SMA_{ma_2}'][i-1] and cash > 0:
        position = position + portfolio_allocation * cash / price
        cash = cash - position * price
    elif asset_data[f'SMA_{ma_1}'].iloc[i] <= asset_data[f'SMA_{ma_2}'][i] and asset_data[f'SMA_{ma_1}'].iloc[i-1] >= asset_data[f'SMA_{ma_2}'][i-1] and position > 0:
        position = position - portfolio_allocation * cash / price
        cash = cash + position * price
    else:
        pass
    cash_1.append(cash)
    equity_1.append(cash + position * price)

asset_data['Cash_1'] = cash_1
asset_data['Equity_1'] = equity_1

profit = round(asset_data['Equity_1'].iloc[-1] - cash_0, 1)

fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))

# Plot data on the first subplot
axs[0].plot(asset_data[f'SMA_{ma_1}'], label=f'SMA_{ma_1}')
axs[0].plot(asset_data[f'SMA_{ma_2}'], label=f'SMA_{ma_2}')
axs[0].set_xlabel('Date')
axs[0].set_ylabel('Value')
axs[0].legend()

# Plot data on the second subplot
axs[1].plot(asset_data['Equity_1'], label='Equity')
axs[1].plot(asset_data['Cash_1'], label='Cash')
axs[1].set_xlabel('Date')
axs[1].set_ylabel('Value')
axs[1].legend()

# Plot data on the third subplot
axs[2].plot(asset_data['Close'], label='Close Price')
axs[2].set_xlabel('Date')
axs[2].set_ylabel('Value')
axs[2].legend()

# Adjust layout to prevent overlap
plt.tight_layout()
plt.subplots_adjust(top=0.9)

# Set a title for the entire figure
fig.suptitle(f'Financial Analysis: {ticker}, Profit: £{profit}', fontsize=16)

plt.show()

print('test')