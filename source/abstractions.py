import datetime

import pandas
import pandas as pd
import numpy as np
from typing import *

# Data Classes
class Lookback:
    def __init__(self, start_date: str, end_date: str, step: str, rolling_lookback: int=252):
        self.start_date = start_date
        self.end_date = end_date
        self.step = step
        self.rolling_lookback = rolling_lookback

class RiskManagement:
    def __init__(self, order: str, take_profit: float, stop_loss: float, market_on_close: str):
        self.order = order
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.market_on_close = market_on_close

class Trade:
    def __init__(self, ticker: str, execution: str, risk_management: RiskManagement):
        self.ticker = ticker
        self.execution = execution
        self.risk_management = risk_management

class TradeStructure:
    def __init__(self, longs: List[Trade], shorts: List[Trade]):
        self.longs = longs
        self.shorts = shorts

class DataPoint:
    def __init__(self, symbol: str, multiplier: float):
        self.symbol = symbol
        self.multiplier = multiplier

class Indicator:
    def __init__(self, positives: List[DataPoint], negatives: List[DataPoint], aggregation: str, price_type: str, threshold_type: str, 
    threshold: float, trigger_type: str, trigger_bias: str, time_filter_unit: str = None, time_filter: list = None):
        self.positives = positives
        self.negatives = negatives
        self.aggregation = aggregation
        self.price_type = price_type
        self.threshold_type = threshold_type
        self.threshold = threshold
        self.trigger_type = trigger_type
        self.trigger_bias = trigger_bias
        self.time_filter_unit = time_filter_unit
        self.time_filter = time_filter

class Signals:
    def __init__(self, indicators: List[Indicator], combination: int):
        self.indicators = indicators
        self.combination = combination

class Backtest:
    def __init__(self, lookback : Lookback, trade_structure : TradeStructure, signals : Signals):
        self.lookback = lookback
        self.trade_structure = trade_structure
        self.signals = signals

class RollingStandardDeviation:
    def __init__(self, sum: float, sum_squared: float, mean: float, N: int, last : float):
        if N <= 0:
            raise Exception("N must be a positive integer")
        self.sum_squared = sum_squared
        self.sum = sum
        self.mean = mean
        self.N = N
        self.sd = self.calculate_sd()
        self.last = last
    def calculate_sd(self):
        return ((self.sum_squared - 2 * self.mean * self.sum + self.mean * self.mean * self.N) / self.N) ** 0.5
    def replace(self, new_val: float, new_last: float):
        self.sum += new_val - self.last
        self.sum_squared += new_val ** 2 - self.last ** 2
        self.mean = self.sum / self.N
        self.sd = self.calculate_sd()
        self.last = new_last
    def add(self, new_val):
        self.N += 1
        self.sum_squared += new_val * new_val
        self.sum += new_val
        self.mean = self.sum / self.N
        self.sd = self.calculate_sd()
# Backtest classes

class RunningTrade:
    def __init__(self, order: str, ticker: str, market_on_close: datetime.datetime, last: float, is_long: bool, stop_loss: float = None, take_profit: float = None):
        self.order = order
        self.ticker = ticker
        self.market_on_close = market_on_close
        self.last = last
        self.is_long = is_long
        self.stop_loss = stop_loss
        self.take_profit = take_profit

class RunningTrades:
    def __init__(self, trades: List[RunningTrade]):
        self.trades = trades
        self.cancel = False
        self.pnl = 0.0

class PriceUpdate:
    def __init__(self, close: float, open: float=None, high: float=None, low: float=None):
        self.close = close
        self.open = open
        self.high = high
        self.low = low

class PriceUpdates:
    def __init__(self, updates: Dict[str, PriceUpdate]):
        self.updates = updates

class Dictionaries:
    def __init__(self, tickers: List[str], percent_dict: Dict[str, Dict[int, RollingStandardDeviation]], average_dict: Dict[str, RollingStandardDeviation]):
        self.tickers = tickers
        self.percent_dict = percent_dict
        self.average_dict = average_dict


# Backtester methods
PATH = "../processed_data/{}.csv"

OPEN = "{}_Open"
CLOSE = "{}_Close"
HIGH = "{}_High"
LOW = "{}_Low"
WANTED_PRICES = ["High", "Low", "Open", "Close"]
DATE_FORMAT = "%m-%d-%Y"

# Walk methods
def update_trade(running_trades: RunningTrades, price_updates: PriceUpdates, performance_data: pd.DataFrame, date: str):
    if running_trades is None:
        return
    trades = running_trades.trades
    for trade in trades:
        update_pnl = None
        price = price_updates.updates[trade.ticker]
        # Checks if price.close exists
        if np.isnan(price.close): 
            return
        if (trade.order == "MOC"):
            update_pnl = (price.close - trade.last) / trade.last if trade.is_long else (trade.last - price.close) / trade.last
            performance_data.loc[performance_data.Date == date, "PnL"] *= update_pnl + 1
            # Hits cut date
            if (datetime.datetime.strptime(date, DATE_FORMAT) >= trade.market_on_close): 
                running_trades.cancel = True
        elif (trade.order == "SLMOC"):
            # Hits stop loss on long side
            if trade.is_long and price.low <= trade.stop_loss:
                update_pnl = (trade.stop_loss - trade.last) / trade.last
                running_trades.cancel = True
            # Hits stop loss on short side
            elif not trade.is_long and price.high >= trade.stop_loss:
                update_pnl = (trade.last - trade.stop_loss) / trade.last
                running_trades.cancel = True
            # Doesn't hit stop
            else:
                update_pnl = (price.close - trade.last) / trade.last if trade.is_long else (trade.last - price.close) / trade.last
                running_trades.cancel = False
            
            performance_data.loc[performance_data.Date == date, "PnL"] *= update_pnl + 1
            # Hits cut date
            if (datetime.datetime.strptime(date, DATE_FORMAT) >= trade.market_on_close):
                running_trades.cancel = True
        elif (trade.order == "OCO"):
            # Hits stop loss on long side
            if trade.is_long and price.low <= trade.stop_loss:
                update_pnl = (trade.stop_loss - trade.last) / trade.last
                running_trades.cancel = True
            # Hits stop loss on short side
            elif not trade.is_long and price.high >= trade.stop_loss:
                update_pnl = (trade.last - trade.stop_loss) / trade.last
                running_trades.cancel = True
            # Hits take profit on long side
            elif trade.is_long and price.high >= trade.take_profit:
                update_pnl = (trade.take_profit - trade.last) / trade.last
                running_trades.cancel = True
            # Hits take profit on short side
            elif not trade.is_long and price.low <= trade.stop_loss:
                update_pnl = (trade.last - trade.take_profit) / trade.last
                running_trades.cancel = True
            # Doesn't hit stop or take
            else:
                update_pnl = (price.close - trade.last) / trade.last if trade.is_long else (trade.last - price.close) / trade.last
                running_trades.cancel = False
            
            performance_data.loc[performance_data.Date == date, "PnL"] *= update_pnl + 1
            # Hits cut date
            if (datetime.datetime.strptime(date, DATE_FORMAT) >= trade.market_on_close):
                running_trades.cancel = True
        trade.last = price.close

def average_to_sum(indicator: Indicator):
    if indicator.aggregation == "average":
        indicator.threshold *= (len(indicator.positives) + len(indicator.negatives))
        indicator.aggregation = "sum"
    return indicator

def signal_recognize(row: pd.DataFrame, signal: Signals, average_dic: Dict[str, RollingStandardDeviation]):
    cnt = 0
    # ASSUMPTIONS - assume aggregation is sum, trigger Type is filter
    for indicator in signal.indicators:
        current_sum = 0
        indicator = average_to_sum(indicator)
        mean = 0
        std = 0
        for positive in indicator.positives:
            current_sum += row[CLOSE.format(positive.symbol)] * positive.multiplier
            mean += average_dic[positive.symbol].mean * positive.multiplier
            std += (average_dic[positive.symbol].sd * positive.multiplier) ** 2
        for negative in indicator.negatives:
            current_sum -= row[CLOSE.format(negative.symbol)] * negative.multiplier
            mean -= average_dic[negative.symbol].mean * negative.multiplier
            std += (average_dic[negative.symbol].sd * negative.multiplier) ** 2
        std = std ** 0.5
        mean /= (len(indicator.positives) + len(indicator.negatives))
        if np.isnan(std):
            raise Exception(row["Date"])
        if ((current_sum - mean) / std) > indicator.threshold and indicator.trigger_bias == 'above':
            cnt += 1
        if ((current_sum - mean) / std) < indicator.threshold and indicator.trigger_bias == 'below':
            cnt += 1
    if cnt  >= signal.combination:
        return True
    return False


def walk(data: pd.DataFrame, backtest: Backtest, percent_change_dic: Dict[str, Dict[int, RollingStandardDeviation]], average_dic: Dict[str, RollingStandardDeviation], performance_data: pd.DataFrame, time_horizons: List[int]):
    trades = None
    for index, row in data[backtest.lookback.rolling_lookback + 35:].iterrows():
        running_trade_list = []
        if not all(row[CLOSE.format(key.ticker)] for key in (backtest.trade_structure.longs + backtest.trade_structure.shorts)):
            raise Exception("Data was not filled")
        if signal_recognize(row, backtest.signals, average_dic) and trades is None:
            for long in backtest.trade_structure.longs:
                risk_management = long.risk_management
                running_trade_list.append(RunningTrade(order = risk_management.order,
                                                       ticker = long.ticker,
                                                       market_on_close = datetime.datetime.strptime(row["Date"], DATE_FORMAT) + datetime.timedelta(days=risk_management.market_on_close),
                                                       is_long = True,
                                                       stop_loss = (1 + percent_change_dic[long.ticker][5].sd * risk_management.stop_loss) * row[CLOSE.format(long.ticker)],
                                                       take_profit = (1 + percent_change_dic[long.ticker][5].sd * risk_management.take_profit) * row[CLOSE.format(long.ticker)],
                                                       last = row[CLOSE.format(long.ticker)]))
            for short in backtest.trade_structure.shorts:
                risk_management = short.risk_management
                running_trade_list.append(RunningTrade(order = risk_management.order,
                                                       ticker = short.ticker,
                                                       market_on_close = datetime.datetime.strptime(row["Date"], DATE_FORMAT) + datetime.timedelta(days=risk_management.market_on_close),
                                                       is_long = False,
                                                       stop_loss = (1 + percent_change_dic[long.ticker][5].sd * risk_management.stop_loss) * row[CLOSE.format(short.ticker)],
                                                       take_profit = (1 + percent_change_dic[long.ticker][5].sd * risk_management.take_profit) * row[CLOSE.format(short.ticker)],
                                                       last = row[CLOSE.format(short.ticker)]))
            running_trades_object = RunningTrades(running_trade_list)
            trades = running_trades_object
            performance_data.loc[performance_data.Date == row["Date"], "Signal"] = True
        else: 
            performance_data.loc[performance_data.Date == row["Date"], "Signal"] = False
        updates = {}
        for sec in backtest.trade_structure.longs + backtest.trade_structure.shorts:
            updates[sec.ticker] = PriceUpdate(close=row[CLOSE.format(sec.ticker)],
                                              open=row[OPEN.format(sec.ticker)],
                                              high=row[HIGH.format(sec.ticker)],
                                              low=row[LOW.format(sec.ticker)])
        price_updates = PriceUpdates(updates)
        for key in average_dic:
            average_dic[key].replace(row[CLOSE.format(key)], data[CLOSE.format(key)][index - backtest.lookback.rolling_lookback + 1])
        for key in percent_change_dic:
            for time_horizon in time_horizons:
                percent_change_dic[key][time_horizon].replace(row[CLOSE.format(key)] / data[CLOSE.format(key)][index - time_horizon], data[CLOSE.format(key)][index - backtest.lookback.rolling_lookback + 1] / data[CLOSE.format(key)][index - backtest.lookback.rolling_lookback + 1 - time_horizon])
        if trades is not None: 
            update_trade(trades, price_updates, performance_data, row["Date"])
        if trades is not None and trades.cancel:
            trades = None
