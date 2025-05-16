import pandas as pd
import numpy as np


def fill_missing_symbol_prices(stock_data, trade_data, symbols):
    close_df = stock_data['Close']
    for sym in symbols:
        # Check if the symbol column exists AND if it's mostly NaN
        if sym not in close_df.columns:
            continue  # symbol missing completely, skip or handle separately
        if close_df[sym].notna().sum() > 5:
            # Enough data points exist, no need to interpolate
            continue
        
        # Now do interpolation for this symbol (mostly NaN column)
        sym_trades = trade_data[trade_data['symbol'] == sym].sort_values('date')
        
        buy_trades = sym_trades[sym_trades['side'] == 'buy']
        sell_trades = sym_trades[sym_trades['side'] == 'sell']

        if buy_trades.empty:
            continue
        
        buy_date = pd.to_datetime(buy_trades.iloc[0]['date'])
        buy_price = buy_trades.iloc[0]['price']

        if sell_trades.empty:
            sell_date = close_df.index[-1]
            sell_price = buy_price
        else:
            sell_date = pd.to_datetime(sell_trades.iloc[-1]['date'])
            sell_price = sell_trades.iloc[-1]['price']

        # Create date range from buy to sell date
        date_range = pd.date_range(start=buy_date, end=sell_date, freq='D')

        # Create linear price interpolation
        prices = np.linspace(buy_price, sell_price, len(date_range))

        # Build a series and align with stock_data's index
        interp_series = pd.Series(prices, index=date_range).reindex(close_df.index)

        # Forward and backward fill missing dates within range
        interp_series = interp_series.fillna(method='ffill').fillna(method='bfill')

        # Replace the column with this interpolated series
        close_df[sym] = interp_series

    # Return updated stock_data with replaced 'Close' DataFrame
    stock_data['Close'] = close_df
    return stock_data
