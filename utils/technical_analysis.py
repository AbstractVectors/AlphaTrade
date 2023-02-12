import pandas
from ta import add_all_ta_features
from ta.utils import dropna
from ta.volatility import AverageTrueRange, BollingerBands
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator, WilliamsRIndicator
from ta.others import DailyReturnIndicator, DailyLogReturnIndicator


acronyms = ['ATR', 'BB', 'SMA', 'EMA', 'MACD', 'RSI', 'SR', 'WR', 'DR', 'DLR']
indicators = [AverageTrueRange, BollingerBands, SMAIndicator, EMAIndicator, MACD, RSIIndicator, StochasticOscillator, WilliamsRIndicator, DailyReturnIndicator, DailyLogReturnIndicator]
functions = ['average_true_range', 'bollinger_mavg', 'sma_indicator', 'ema_indicator', 'macd', 'rsi', 'stoch', 'williams_r', 'daily_return', 'daily_log_return']
params = [('high', 'low', 'close'), ('close',), ('close', 'window'), ('close',), ('close',), ('close',), ('high', 'low', 'close'), ('high', 'low', 'close'), ('close',)]

def run_tech(df: pandas.DataFrame, indicator_aronym: str) -> pandas.DataFrame:
    if indicator_aronym not in acronyms:
        df = add_all_ta_features(dropna(df), open="Open", high="High", low="Low", close="Close", volume="Volume_BTC")
        return df
    # df = dropna(data)
    window = 20
    high = df['High']
    low = df['Low']
    close = df['Close']
    index = acronyms.index(indicator_aronym)
    param_str = []
    for param in params[index]:
        param_str.append('{}={}'.format(param, param))
    exec('indicator = indicators[index]({})'.format(', '.join(param_str)))
    df[indicator_aronym] = eval('indicator.{}()'.format(functions[index]))
    return df
