import pandas as pd
from typing import *
import os
import datetime

RDIR = "../processed_data"
AGG_DATA_PATH = "../aggregated_data/agg_data.csv"
AGG_FILES_PATH = "../aggregated_data/agg_files.txt"

WANTED_PRICES = ["High", "Low", "Open", "Close"]
DATE_FORMAT = "%m-%d-%Y"

agg_files = open(AGG_FILES_PATH, "r")
added_files = agg_files.read().split()
agg_files.close()

agg_data = pd.read_csv(AGG_DATA_PATH)

dates = []

date = datetime.datetime(1995, 12, 31)
while date < datetime.datetime.today():
    date += datetime.timedelta(days=1)
    if date.weekday() >= 5:
        continue
    dates.append(date.strftime(DATE_FORMAT))


agg_data["Date"] = dates

counter = 0
for filename in os.listdir(RDIR):
    file = os.path.join(RDIR, filename)
    if os.path.isfile(file) and filename not in added_files and not filename.startswith("."):
        print(filename, file)
        merge_data = pd.read_csv(file)
        columns = list(merge_data.columns)
        cols = list(set(WANTED_PRICES) & set(columns))
        for col in WANTED_PRICES:
            agg_data[filename.split(".")[0] + "_" + col] = ""
        for ind, row in merge_data.iterrows():
            for col in cols:
                #print(filename.split(".")[0] + "_" + col)
                agg_data.loc[agg_data.Date == row["Date"], filename.split(".")[0] + "_" + col] = row[col]
        added_files.append(filename)
        counter += 1

agg_files = open(AGG_FILES_PATH, "w")
agg_files.writelines(added_files)
agg_files.close()
agg_data.to_csv(AGG_DATA_PATH, index=None)

'''
def merge_trade_data(source_data: pd.DataFrame, securities: List[Trade], long: bool=False, short: bool=False):
    for sec in securities:
        risk_management = sec.risk_management
        merge_data = pd.read_csv(PATH.format(sec.ticker))
        columns = list(merge_data.columns)
        cols = list(set(WANTED_PRICES) & set(columns))
        if not "Close" in columns:
            raise Exception(sec.ticker + " does not have close price")
        else:
            source_data[CLOSE.format(sec.ticker)] = ""
        if "Open" in columns:
            source_data[OPEN.format(sec.ticker)] = ""
        if "High" in columns:
            source_data[HIGH.format(sec.ticker)] = ""
        elif long and risk_management.order == "OCO":
            raise Exception(sec.ticker + " cannot have long OCO order without high")
        elif short and risk_management.order != "MOC":
            raise Exception(short.ticker + " cannot have short non-MOC order without high")
        if "Low" in columns:
            source_data[LOW.format(sec.ticker)] = ""
        elif long and risk_management.order != "MOC":
            raise Exception(sec.ticker + " cannot have long non-MOC order without low")
        elif short and risk_management.order == "OCO":
            raise Exception(short.ticker + " cannot have short OCO order without low")
        for ind, row in merge_data.iterrows():    
            for col in cols:
                source_data.loc[source_data.date == row["Date"], sec.ticker + "_" + col] = row[col]

def merge_symbol_data(source_data: pd.DataFrame, symbols: List[DataPoint]):
    for symbol in symbols:
        merge_data = pd.read_csv(PATH.format(symbol.symbol))
        columns = list(merge_data.columns)
        cols = list(set(WANTED_PRICES) & set(columns))
        for ind, row in merge_data.iterrows():    
            for col in cols:
                source_data.loc[source_data.date == row["Date"], symbol.symbol + "_" + col] = row[col]
'''