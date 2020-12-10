# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import yfinance as yf
import streamlit as st

trade_data = pd.read_csv('./data/trade.csv', sep=';')
symbols = trade_data['symbol'].unique().tolist()
trade_dates = trade_data['date'].unique().tolist()
symbols_str = " ".join(symbols)
stock_data = yf.download(symbols_str, start=min(trade_data['date']))

dates = stock_data.index.tolist()
amount_dic = {k: 0 for k in symbols}
cash = 605
value_total_list = []
cash_list = []
value_stock_list = []

for date in dates:
    date = date.strftime('%Y-%m-%d')
    if date in trade_dates:
        trades_on_the_date = len(trade_data[trade_data['date'] == date].index)
        for i in range(trades_on_the_date):
            side_i = trade_data[trade_data['date'] == date]['side'].iloc[i]
            amount_i = trade_data[trade_data['date'] == date]['amount'].iloc[i]
            symbol_i = trade_data[trade_data['date'] == date]['symbol'].iloc[i]
            price_i = stock_data.loc[date]['Adj Close'][symbol_i]
            if side_i == 'buy':
                cash = cash - amount_i * price_i
                amount_dic[symbol_i] = amount_dic[symbol_i] + amount_i
            else:
                cash = cash + amount_i * price_i
                amount_dic[symbol_i] = amount_dic[symbol_i] - amount_i
    value_stock = 0
    for symbol in amount_dic:
        value_stock = value_stock + amount_dic[symbol] * stock_data.loc[date]['Adj Close'][symbol]
    value_total = cash + value_stock
    value_total_list.append(value_total)
    cash_list.append(cash)
    value_stock_list.append(value_stock)

df = pd.DataFrame({
    'date': dates,
    'cash (USD)': cash_list,
    'stock (USD)': value_stock_list,
    'total (USD)': value_total_list
})
df = df.set_index('date')

st.title('Shabby ETF')
st.write("Performance:")
st.line_chart(df)
st.write("Stock position history:")
st.write(trade_data)