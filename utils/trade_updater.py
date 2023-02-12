from abstractions import *
import pandas as pd
from typing import *


def update_trade(running_trades: RunningTrades, price_updates: PriceUpdates, performance_data: pd.DataFrame, date: datetime.datetime):
    trades = running_trades.trades
    for trade in trades:
        update_pnl = None
        price = price_updates.updates[trade.ticker]
        if (trade.order == "MOC"):
            update_pnl = price.close - trade.last if trade.is_long else trade.last - price.close
            performance_data.loc[performance_data.date == date, "pnl"] += update_pnl
            # Hits cut date
            if (date == trade.market_on_close): running_trades.cancel = True
        elif (trade.order == "SLMOC"):
            # Hits stop loss on long side
            if trade.is_long and price.low <= trade.risk_management.stop_loss:
                update_pnl = trade.risk_management.stop_loss - trade.last
            # Hits stop loss on short side
            elif not trade.is_long and price.high >= trade.risk_management:
                update_pnl = trade.last - trade.risk_management.stop_loss
            # Doesn't hit stop
            else:
                update_pnl = price.close - trade.last if trade.is_long else trade.last - price.close
            
            performance_data.loc[performance_data.date == date, "pnl"] += update_pnl
            # Hits cut date
            if (date == trade.market_on_close): running_trades.cancel = True
        elif (trade.order == "OCO"):
            # Hits stop loss on long side
            if trade.is_long and price.low <= trade.risk_management.stop_loss:
                update_pnl = trade.risk_management.stop_loss - trade.last
            # Hits stop loss on short side
            elif not trade.is_long and price.high >= trade.risk_management.stop_loss:
                update_pnl = trade.last - trade.risk_management.stop_loss
            # Hits take profit on long side
            elif trade.is_long and price.high >= trade.risk_management.take_profit:
                update_pnl = trade.risk_management.take_profit - trade.last
            # Hits take profit on short side
            elif not trade.is_long and price.low <= trade.risk_management.stop_loss:
                update_pnl = trade.last - trade.risk_management.take_profit
            # Doesn't hit stop or take
            else:
                update_pnl = price.close - trade.last if trade.is_long else trade.last - price.close
            
            performance_data.loc[performance_data.date == date, "pnl"] += update_pnl
            # Hits cut date
            if (date == trade.market_on_close): running_trades.cancel = True


