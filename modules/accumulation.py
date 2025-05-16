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
                price_i = stock_data.loc[date]['Close'][symbol_i]
                if side_i == 'buy':
                    cash = cash - amount_i * price_i
                    amount_dic[symbol_i] = amount_dic[symbol_i] + amount_i
                else:
                    cash = cash + amount_i * price_i
                    amount_dic[symbol_i] = amount_dic[symbol_i] - amount_i
        value_stock = 0
        for symbol in amount_dic:
            value_stock = value_stock + amount_dic[symbol] * stock_data.loc[date]['Close'][symbol]
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
                last_value_total=value_total,
                second_last_value_total = value_total_list[-2])