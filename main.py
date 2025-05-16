import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.express as px
from modules.fill_missing_symbol_prices import fill_missing_symbol_prices
from modules.accumulation import accumulation
from modules.current_position_calculation import current_position_calculation


if __name__ == "__main__":
    # 1. Calculate accumulative ROI
    trade_data = pd.read_csv('./data/trade.csv', sep=';')
    symbols = trade_data['symbol'].unique().tolist()
    trade_dates = trade_data['date'].unique().tolist()
    symbols_str = " ".join(symbols)
    stock_data = yf.download(symbols_str, start='2020-12-09')
    stock_data = fill_missing_symbol_prices(stock_data, trade_data, symbols)
    dates = stock_data.index.tolist()
    amount_dic = {k: 0 for k in symbols}
    # cash = 605
    cash = 0

    results = accumulation(trade_data, trade_dates, stock_data, dates, amount_dic, cash)

    df = pd.DataFrame({
        'date': dates,
        'total (USD)': results['value_total_list']
    })
    df = df.set_index('date')

    # 2. Calculate the current position
    current_position = current_position_calculation(results['last_amount_dic'],
                                                    results['last_date'],
                                                    results['last_cash'],
                                                    stock_data)
    # used_cash = -current_position[current_position['component'] == 'cash']['value'].values[0]
    # deviation = round((results['last_value_total'] / cash - 1) * 100, 1)
    deviation = round(results['last_value_total'] - cash, 0)
    # deviation_today = round((results['last_value_total'] / results['second_last_value_total'] - 1) * 100, 1)
    deviation_today = round(results['last_value_total'] - results['second_last_value_total'], 0)

    # 3. Visualize the portfolio
    # fig = px.pie(current_position, values='value', names='component')
    fig = px.pie(current_position[current_position['value'] > 0], values='value', names='component')
    st.title('Shabby ETF ($SHAB)')
    # st.write('All %: ' + str(deviation) + "%")
    st.write('All: ' + str(deviation) + ' USD')
    # st.write('1 Day %: ' + str(deviation_today) + '%')
    st.write('1 Day: ' + str(deviation_today) + ' USD')
    st.write("Asset Net Worth:")
    st.line_chart(df)
    st.write("Asset Allocation:")
    st.write(fig)
    st.write("Transaction History:")
    st.write(trade_data)