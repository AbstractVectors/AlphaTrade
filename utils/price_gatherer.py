# DEPRECATED

import pandas as pd
import json
import requests
import datetime
import time

start_date = datetime.datetime.now()
target_date = datetime.datetime(2020, 1, 1)
ticker = input("Input the ticker: ")
time_interval = input("Input the time interval: ")
time_unit = input("Input the time unit (minute, hour, day): ")
#unit_dict = {"minute": 1, "hour": 60, "day": 1440}

BASE = "https://api.polygon.io/v2/aggs/ticker/{}/range/{}/{}/{}/{}?adjusted=true&sort=asc&limit=50000&apiKey=2CiMnHo26Rsl7EfHzQHNnASWAHcKUvLB"
PATH = "../data/{}_{}_{}.csv"

b=1
df = pd.DataFrame(columns=['v', 'vw', 'o', 'c', 'h', 'l', 't', 'n'])
while (start_date >= target_date and b):
    end_date = start_date - datetime.timedelta(days=33)
    if (end_date <= datetime.datetime(2021, 1, 1)):
        end_date = datetime.datetime(2021, 1, 1)
        b=0
    #print(end_date.strftime("%Y-%m-%d"))
    print(BASE.format(ticker, time_interval, time_unit, end_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d")))
    resp = requests.get(BASE.format(ticker, time_interval, time_unit, end_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d")))
    my_dic = resp.json()
    #print(my_dic.keys())
    my_df = pd.DataFrame(my_dic["results"])
    print(my_df)
    df = pd.concat([my_df, df]).reset_index(drop=True)
    time.sleep(15)
    start_date = end_date - datetime.timedelta(days=1)

#print(df)

path = PATH.format(ticker, time_interval, time_unit)
try:
    open(path, 'x')
except:
    pass
file = open(path, 'w')

df.rename(
    columns=({ 'v': 'volume', 
               'vw': 'volume_weighted_average_price',
               'o': 'open',
               'c': 'close',
               'h': 'high',
               'l': 'low',
               't': 'time',
               'n': 'number_transactions'}), 
    inplace=True,
)
df.to_csv(file, index=False)