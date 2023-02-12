import pandas
import numpy as np

def pnl_cum_sum(df: pandas.DataFrame):
    l = []
    cum_sum = 0
    for n in df['PnL']:
        if not np.isnan(n): 
            cum_sum += (n - 1) * 100
        l.append(cum_sum)
    df['cum_sum'] = l
    return df