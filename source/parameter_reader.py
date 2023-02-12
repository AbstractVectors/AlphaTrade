import pandas as pd
import pickle
import json
import datetime
from source.abstractions import *

DATE_FORMAT = "%m-%d-%Y"

# Used for lookback
LOOKBACK_KEYS = ["startDate", "endDate", "step", "rollingLookbackPeriod"]

# Used for tradeStructure validation
SEC_KEYS = ["ticker", "execution", "riskManagement"]
ORDER_TYPES = ["OCO", "SLMOC", "MOC"]

# Used for signals validation
AGGREGATION_TYPES = ["sum", "average"]
PRICE_TYPES = ["absolute", "percent"]
THRESHOLD_TYPES = ["level", "zscore"]
TRIGGER_TYPES = ["filter", "break"]
TRIGGER_BIASES = ["above", "below"]
TIME_FILTER_UNITS = ["minute", "hour", "day", "week", "month", "year"]

# Data validation for lookback
def validate_lookback(lookback):
    if not all(key in lookback and lookback[key] for key in LOOKBACK_KEYS):
        raise Exception("Lookback must have all fields populated")
    else:
        start_date = None
        end_date = None
        try:
            start_date = datetime.datetime.strptime(lookback["startDate"], DATE_FORMAT)
        except:
            raise Exception("Invalid startDate format (expected %m-%d-%Y but got " + lookback["startDate"] + ")")
        try:
            end_date = datetime.datetime.strptime(lookback["endDate"], DATE_FORMAT)
        except:
            raise Exception("Invalid endDate format (expected %m-%d-%Y but got " + lookback["endDate"] + ")")
        if (start_date >= end_date):
            raise Exception("startDate must come before endDate")
        if not isinstance(lookback["step"], int):
            raise Exception("Lookback has invalid step datatype (expected <class 'int'> but got " + str(type(lookback["step"])) + ")")
        if start_date - datetime.timedelta(days=lookback["rollingLookbackPeriod"]+35) <= datetime.datetime(2008, 1, 1):
            raise Exception("Total lookback can't go before 2008")
        
    return Lookback(lookback["startDate"], lookback["endDate"], lookback["step"], lookback["rollingLookbackPeriod"])

# Data validation for tradeStructure
# Checks that there is at least 1 security in the tradeStructure object
def validate_trade_structure(trade_structure):
    if not len(trade_structure["short"]) and not len(trade_structure["long"]):
        raise Exception("Both long and short cannot be empty")
    longs = []
    shorts = []
    validate_security(trade_structure, "long", longs)
    validate_security(trade_structure, "short", shorts)
    return TradeStructure(longs, shorts)

def validate_security(trade_structure, bias, securities):
    for sec in trade_structure[bias]:
        # Checks that the security object is populated
        if not all(key in sec and sec[key] for key in SEC_KEYS):
            raise Exception("Each security must be populated with ticker, execution, riskManagement")
        
        ticker = sec["ticker"]
        risk_management = sec["riskManagement"]
        order = risk_management["order"]
        take_profit = risk_management["takeProfit"]
        stop_loss = risk_management["stopLoss"]
        market_on_close = risk_management["marketOnClose"]


        # Checks that the security object has a valid order type
        if order not in ORDER_TYPES:
            raise Exception(ticker + " has invalid order type (expected OCO or SLMOC or MOC but got " + order + ")")

        # Given a valid order type, checks that the fields are populated with appropriate datatypes and formats
        if order == "OCO":
            if not isinstance(take_profit, float):
                raise Exception(ticker + " has invalid takeProfit datatype (expected <class 'float'> but got " + str(type(take_profit)) + ")")
            if not isinstance(stop_loss, float):
                raise Exception(ticker + " has invalid stopLoss datatype (expected <class 'float'> but got " + str(type(stop_loss)) + ")")
            if not isinstance(market_on_close, int):
                raise Exception(ticker + " has invalid marketOnClose datatype (expected <class 'int'> but got " + str(type(market_on_close)) + ")")
        elif order == "SLMOC":
            if take_profit:
                raise Exception(ticker + " has invalid takeProfit parameter (expected \"\" but got " + take_profit + ")")
            if not isinstance(stop_loss, float):
                raise Exception(ticker + " has invalid stopLoss datatype (expected <class 'float'> but got " + str(type(stop_loss)) + ")")
            if not isinstance(market_on_close, int):
                raise Exception(ticker + " has invalid marketOnClose datatype (expected <class 'int'> but got " + str(type(market_on_close)) + ")")
        elif order == "MOC":
            if take_profit:
                raise Exception(ticker + " has invalid takeProfit parameter (expected \"\" but got " + take_profit + ")")
            if stop_loss:
                raise Exception(ticker + " has invalid stopLoss parameter (expected \"\" but got " + stop_loss + ")")
            if not isinstance(market_on_close, int):
                raise Exception(ticker + " has invalid marketOnClose datatype (expected <class 'int'> but got " + str(type(market_on_close)) + ")")
        securities.append(Trade(ticker, sec["execution"], RiskManagement(order, take_profit, stop_loss, market_on_close)))
            

# Data validation for signals
def validate_signals(signals):
    indicators = []
    for indicator in signals["indicators"]:
        pos = indicator["positive"]
        neg = indicator["negative"]
        positives = []
        negatives = []

        for symbol in pos:
            if not symbol["symbol"]:
                raise Exception("Each positive indicator must be populated with a symbol")
            if symbol["multiplier"] and not isinstance(symbol["multiplier"], float):
                raise Exception(symbol["symbol"] + " has invalid multiplier (expected \"\" OR <class 'float'> but got " + symbol["multiplier"] + ")")
            positives.append(DataPoint(symbol["symbol"], symbol["multiplier"]))

        for symbol in neg:
            if not symbol["symbol"]:
                raise Exception("Each positive indicator must be populated with a symbol")
            if symbol["multiplier"] and not isinstance(symbol["multiplier"], float):
                raise Exception(symbol["symbol"] + " has invalid multiplier (expected \"\" OR <class 'float'> but got " + symbol["multiplier"] + ")")
            negatives.append(DataPoint(symbol["symbol"], symbol["multiplier"]))
            
        if indicator["aggregation"] not in AGGREGATION_TYPES:
            raise Exception("Indicator has invalid aggregation (expected \"sum\" OR \"average\" but got " + indicator["aggregation"] + ")")
        if indicator["priceType"] not in PRICE_TYPES:
            raise Exception("Indicator has invalid priceType (expected \"absolute\" OR \"percent\" but got " + indicator["priceType"] + ")")
        if indicator["thresholdType"] not in THRESHOLD_TYPES:
            raise Exception("Indicator has invalid thresholdType (expected \"level\" OR \"zscore\" but got " + indicator["thresholdType"] + ")")
        if not isinstance(indicator["threshold"], float):
            raise Exception("Indicator has invalid threshold datatype (expected <class 'float'> but got " + str(type(indicator["threshold"])) + ")")
        if indicator["triggerType"] not in TRIGGER_TYPES:
            raise Exception("Indicator has invalid triggerType (expected \"filter\" OR \"break\" but got " + indicator["triggerType"] + ")")
        if indicator["triggerBias"] not in TRIGGER_BIASES:
            raise Exception("Indicator has invalid triggerBias (expected \"above\" OR \"below\" but got " + indicator["triggerBias"] + ")")
        #if indicator["timeFilterUnit"] and indicator["timeFilterUnit"] not in TIME_FILTER_UNITS:
        #    raise Exception("Indicator has invalid timeFilterUnit")
        indicators.append(Indicator(positives, negatives,
                                indicator["aggregation"], indicator["priceType"],
                                indicator["thresholdType"], indicator["threshold"],
                                indicator["triggerType"], indicator["triggerBias"]))
                                #indicator["timeFilterUnit"], indicator["timeFilter"])) 
    if not isinstance(signals["combination"], int):
        raise Exception("Signals has invalid combination (expected <class 'int'> but got " + str(type(signals["combination"])) + ")")
    return Signals(indicators, signals["combination"])