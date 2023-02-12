import yfinance as yf

def get_data(symbol, period='max', interval='1d', start=None, end=None):
    '''
    Help on function get_data:

    get_data(symbol, period='max', interval='1d', start=None, end=None)
        :Parameters:
            symbol : str
                Ticker symbol of stock
            period : str
                Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                Either Use period parameter or use start and end
            interval : str
                Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                Intraday data cannot extend last 60 days
            start: str
                Download start date string (YYYY-MM-DD) or _datetime.
                Default is 1900-01-01
            end: str
                Download end date string (YYYY-MM-DD) or _datetime.
                Default is now
    '''
    symbol = symbol.upper()
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period, interval=interval, start=start, end=end)
    # data.to_csv('../raw_data/{}.csv'.format(symbol))
    return data
