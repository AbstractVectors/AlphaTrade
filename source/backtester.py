import pandas as pd
import numpy as np
import datetime
import os
from source.abstractions import *

DATE_FORMAT = "%m-%d-%Y"

def backtest(backtest: Backtest):
    lookback = backtest.lookback
    trade_structure = backtest.trade_structure
    signals = backtest.signals

    agg_data = pd.read_csv("aggregated_data/agg_data.csv")
    #agg_data = agg_data.set_index('Date')

    # Calculate start and end dates for backtest
    start = datetime.datetime.strptime(lookback.start_date, DATE_FORMAT)
    start = start + datetime.timedelta(days=7-start.weekday()) if start.weekday() >= 5 else start
    end = datetime.datetime.strptime(lookback.end_date, DATE_FORMAT)
    end = end + datetime.timedelta(days=7 - end.weekday()) if end.weekday() >= 5 else end
    start_index = agg_data[agg_data.Date == start.strftime(DATE_FORMAT)].index[0]
    end_index = agg_data[agg_data.Date == end.strftime(DATE_FORMAT)].index[0]

    # Extract data
    longs = trade_structure.longs
    shorts = trade_structure.shorts
    positives = []
    negatives = []
    for indicator in signals.indicators:
        for positive in indicator.positives:
            positives.append(positive)
        for negative in indicator.negatives:
            negatives.append(negative)
    

    # Create union of data
    source_data = pd.DataFrame(columns=["Date"])
    dates = []
    date = datetime.datetime.strptime(agg_data["Date"][start_index - lookback.rolling_lookback - 35], DATE_FORMAT)
    while date <= end:
        date += datetime.timedelta(days=1)
        if date.weekday() >= 5:
            continue
        dates.append(date.strftime(DATE_FORMAT))
    source_data["Date"] = dates

    # Place data in union of data
    OPEN = "{}_Open"
    CLOSE = "{}_Close"
    HIGH = "{}_High"
    LOW = "{}_Low"

    securities = list(set(longs + shorts))
    symbols = list(set(positives + negatives))

    source_data_start_index = start_index - lookback.rolling_lookback - 35
    for sec in securities:
        source_data[OPEN.format(sec.ticker)] = ""
        source_data[OPEN.format(sec.ticker)] = agg_data[OPEN.format(sec.ticker)][source_data_start_index : end_index + 1].values
        source_data[CLOSE.format(sec.ticker)] = agg_data[CLOSE.format(sec.ticker)][source_data_start_index : end_index + 1].values
        source_data[HIGH.format(sec.ticker)] = agg_data[HIGH.format(sec.ticker)][source_data_start_index : end_index + 1].values
        source_data[LOW.format(sec.ticker)] = agg_data[LOW.format(sec.ticker)][source_data_start_index : end_index + 1].values

    for symbol in symbols:
        source_data[OPEN.format(symbol.symbol)] = agg_data[OPEN.format(symbol.symbol)][source_data_start_index : end_index + 1].values
        source_data[CLOSE.format(symbol.symbol)] = agg_data[CLOSE.format(symbol.symbol)][source_data_start_index : end_index + 1].values
        source_data[HIGH.format(symbol.symbol)] = agg_data[HIGH.format(symbol.symbol)][source_data_start_index : end_index + 1].values
        source_data[LOW.format(symbol.symbol)] = agg_data[LOW.format(symbol.symbol)][source_data_start_index : end_index + 1].values

    source_data = source_data.fillna(method="ffill")
    source_data.to_csv("./source_data.csv", index=None)

    # Initialize dictionaries
    average_dic = {}
    percent_change_dic = {}
    user_time_horizons = [5]
    time_horizons = [1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35]
    time_horizons = list(set(user_time_horizons) & set(time_horizons))

    # Populate average_dic
    for sec in securities:
        hist_data = list(source_data[CLOSE.format(sec.ticker)][35 : 35 + lookback.rolling_lookback])
        rolling_standard_deviation = RollingStandardDeviation(hist_data[0], hist_data[0] ** 2, hist_data[0], 1, hist_data[0])
        for data in hist_data[1:]:
            rolling_standard_deviation.add(data)
        average_dic[sec.ticker] = rolling_standard_deviation
    
    for symbol in symbols:
        hist_data = list(source_data[CLOSE.format(symbol.symbol)][35 : 35 + lookback.rolling_lookback])
        rolling_standard_deviation = RollingStandardDeviation(hist_data[0], hist_data[0] ** 2, hist_data[0], 1, hist_data[0])
        for data in hist_data[1:]:
            rolling_standard_deviation.add(data)
        average_dic[symbol.symbol] = rolling_standard_deviation
    

    # Populate percent_change_dic
    for sec in securities:
        percent_change_dic[sec.ticker] = dict.fromkeys(time_horizons)
        for time_horizon in time_horizons:
            hist_data = list(source_data[CLOSE.format(sec.ticker)][35 - time_horizon : 35 + lookback.rolling_lookback])
            rolling_standard_deviation = RollingStandardDeviation(hist_data[time_horizon] / hist_data[0], (hist_data[time_horizon] / hist_data[0]) ** 2, hist_data[time_horizon] / hist_data[0], 1, hist_data[time_horizon] / hist_data[0])
            for i in range(1, lookback.rolling_lookback):
                rolling_standard_deviation.add(hist_data[time_horizon + i] / hist_data[i])
            percent_change_dic[sec.ticker][time_horizon] = rolling_standard_deviation
    
    for symbol in symbols:
        percent_change_dic[symbol.symbol] = dict.fromkeys(time_horizons)
        for time_horizon in time_horizons:
            hist_data = list(source_data[CLOSE.format(symbol.symbol)][35 - time_horizon : 35 + lookback.rolling_lookback])
            rolling_standard_deviation = RollingStandardDeviation(hist_data[time_horizon] / hist_data[0], (hist_data[time_horizon] / hist_data[0]) ** 2, hist_data[time_horizon] / hist_data[0], 1, hist_data[time_horizon] / hist_data[0])
            for i in range(1, lookback.rolling_lookback):
                rolling_standard_deviation.add(hist_data[time_horizon + i] / hist_data[i])
            percent_change_dic[symbol.symbol][time_horizon] = rolling_standard_deviation

    performance_data = pd.DataFrame(columns=["Date", "PnL", "Signal"])
    performance_dates = [(start + datetime.timedelta(days=x)).strftime(DATE_FORMAT) for x in range((end - start).days)]
    performance_data["Date"] = performance_dates
    performance_data["PnL"] = 1.0
    performance_data["Signal"] = False

    walk(source_data, backtest, percent_change_dic, average_dic, performance_data, time_horizons)

    return performance_data   