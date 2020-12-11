import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.express as px


def accumulation(trade_data, trade_dates, stock_data, dates, amount_dic, cash):
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
    return dict(value_total_list=value_total_list,
                cash_list=cash_list,
                value_stock_list=value_stock_list,
                last_date=date,
                last_amount_dic=amount_dic,
                last_cash=cash,
                last_value_total=value_total)


def current_position_calculation(amount_dic, date, cash):
    current_symbol_list = []
    current_symbol_value_list = []
    for symbol in amount_dic:
        if amount_dic[symbol] > 0:
            current_symbol_list.append(symbol)
            current_symbol_value_list.append(amount_dic[symbol] * stock_data.loc[date]['Adj Close'][symbol])
    current_position = pd.DataFrame({
        'component': ['cash'] + current_symbol_list,
        'value': [cash] + current_symbol_value_list
    })
    return current_position


if __name__ == "__main__":
    # 1. Calculate accumulative ROI
    trade_data = pd.read_csv('./data/trade.csv', sep=';')
    symbols = trade_data['symbol'].unique().tolist()
    trade_dates = trade_data['date'].unique().tolist()
    symbols_str = " ".join(symbols)
    stock_data = yf.download(symbols_str, start='2020-12-09')
    dates = stock_data.index.tolist()
    amount_dic = {k: 0 for k in symbols}
    cash = 605

    results = accumulation(trade_data, trade_dates, stock_data, dates, amount_dic, cash)

    df = pd.DataFrame({
        'date': dates,
        'cash (USD)': results['cash_list'],
        'stock (USD)': results['value_stock_list'],
        'total (USD)': results['value_total_list']
    })
    df = df.set_index('date')

    # 2. Calculate the current position
    current_position = current_position_calculation(results['last_amount_dic'],
                                                    results['last_date'],
                                                    results['last_cash'])
    deviation = round((results['last_value_total'] / cash - 1) * 100)

    # 3. Visualize the portfolio
    fig = px.pie(current_position, values='value', names='component')
    st.title('Shabby ETF ($SHAB): ' + str(deviation) + "%")
    st.write("Performance:")
    st.line_chart(df)
    st.write("Portfolio:")
    st.write(fig)
    st.write("Transaction Records:")
    st.write(trade_data)