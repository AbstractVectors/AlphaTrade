import pandas as pd
from abstractions import *
from typing import *

DATE_FORMAT = "%m-%d-%Y"
OPEN = "{}_Open"
CLOSE = "{}_Close"
HIGH = "{}_High"
LOW = "{}_Low"

def walk(data: pd.DataFrame, backtest: Backtest, std_dic: Dict[str, Dict[int, float]], vol_dic: Dict[str, float]):
    trades = []
    for index, row in data.iterrows():
        running_trade_list = []
        if not all(row[CLOSE.format(key.ticker)] for key in backtest.trade_structure.longs + backtest.trade_structure.shorts):
            continue
        if signal_recognize(row, backtest.signals):
            for long in backtest.trade_structure.longs:
                risk_management = long.risk_management
                running_trade_list.append(RunningTrade(order = risk_management.order, market_on_close = datetime.datetime.strptime(row["Date"], DATE_FORMAT) + datetime.timedelta(days=risk_management.market_on_close),
                is_long = True, stop_loss = std_dic[long.ticker][14] * risk_management.stop_loss, take_profit = std_dic[long.ticker][14] * risk_management.take_profit, last = row[CLOSE.format(long.ticker)]))
            for short in backtest.trade_structure.shorts:
                risk_management = short.risk_management
                running_trade_list.append(RunningTrade(order = risk_management.order, market_on_close = datetime.datetime.strptime(row["Date"], DATE_FORMAT) + datetime.timedelta(days=risk_management.market_on_close),
                is_long = False, stop_loss = std_dic[long.ticker][14] * risk_management.stop_loss, take_profit = std_dic[long.ticker][14] * risk_management.take_profit, last = row[CLOSE.format(short.ticker)]))
            running_trades_object = RunningTrades(running_trade_list)
            trades.append(running_trades_object)
            data.loc[data.date == row["Date"], "signal"] = True
        else: 
            data.loc[data.date == row["Date"], "signal"] = False
        for trade in trades:
            updates = {}
            for sec in backtest.trade_structure.longs + backtest.trade_structure.shorts:
                updates[sec.ticker] = PriceUpdate(close=row[CLOSE.format(sec.ticker)],
                                                        open=row[OPEN.format(sec.ticker)],
                                                        high=row[HIGH.format(sec.ticker)],
                                                        low=row[LOW.format(sec.ticker)])
            price_updates = PriceUpdates(updates)
            update_trade(trade, price_updates, data, datetime.datetime.strptime(row["Date"], DATE_FORMAT))
        
    