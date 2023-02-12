from abstractions import *
from parameter_reader import *
from backtester import *
import json
from graphClass import *
from graph_util import *

def main(data):
    lookback = data["lookback"]
    trade_structure = data["tradeStructure"]
    signals = data["signals"]

    lookback_data = validate_lookback(lookback)
    trade_structure_data = validate_trade_structure(trade_structure)
    signals_data = validate_signals(signals)

    performance_data = backtest(Backtest(lookback_data, trade_structure_data, signals_data))
    performance_data = pnl_cum_sum(performance_data)
    return performance_data
    

if __name__ == "__main__":
    PATH = "../test/{}.json"
    filename = input("Input the filename: ")
    f = open(PATH.format(filename))
    data = json.load(f)
    performance_data = main(data)
    print(performance_data)
    performance_data.to_csv("./test.csv", index=None)
    pnlvstime = Graph(data = performance_data, x_title = "Date", y_title = "cum_sum", graph_type = "line", ticks = 5, title = "Profit and Loss vs time")
    pnlvstime.graph()