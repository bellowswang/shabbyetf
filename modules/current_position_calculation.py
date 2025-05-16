import pandas as pd


def current_position_calculation(amount_dic, date, cash, stock_data):
    current_symbol_list = []
    current_symbol_value_list = []
    for symbol in amount_dic:
        if amount_dic[symbol] > 0:
            current_symbol_list.append(symbol)
            current_symbol_value_list.append(amount_dic[symbol] * stock_data.loc[date]['Close'][symbol])
    current_position = pd.DataFrame({
        'component': ['cash'] + current_symbol_list,
        'value': [cash] + current_symbol_value_list
    })
    return current_position