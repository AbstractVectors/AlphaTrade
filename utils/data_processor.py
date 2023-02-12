import pandas as pd
import os
import datetime

YFINANCE_DATE_FORMAT = "%m-%d-%Y"
BLOOMBERG_DATE_FORMAT = "%m/%d/%Y"
DATE_FORMAT = "%m-%d-%Y"

rdir = "../raw_data"
wdir = "../processed_data"

for filename in os.listdir(rdir):
    file = os.path.join(rdir, filename)
    if os.path.isfile(file):
        df = pd.read_csv(file)
        dates = df["Date"]
        try:
            datetimes = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in dates]
            datetimes = sorted(datetimes)
            formatted_dates = [date.strftime(DATE_FORMAT) for date in datetimes]
        except:
            datetimes = [datetime.datetime.strptime(date, "%m/%d/%Y") for date in dates]
            datetimes = sorted(datetimes)
            formatted_dates = [date.strftime(DATE_FORMAT) for date in datetimes]
        weekday = [datetime.datetime.strptime(date, DATE_FORMAT).weekday() for date in formatted_dates]
        df["Date"] = formatted_dates
        df["Weekday"] = weekday
        print(df)
        df.to_csv(os.path.join(wdir, filename), index=None, header=True)
        

