import json
import random
my_dic_long = {}
my_dic_long["lookback"] = {"startDate": "06-12-2019", "endDate": "07-15-2019", "step": random.randint(0, 1440)}
my_dic_long["tradeStructure"] = {"long": [{"ticker": "EURUSD=X", "execution": "market", "riskManagement": {
    "order": "OCO", 
     "takeProfit": random.random()*2, 
     "stopLoss": -random.random()*2, 
     "marketOnClose": random.randint(1, 20)
}}], 
"short": []
}
my_dic_long["signals"] = { 
    "indicators" : [{
    "positive": [{"symbol": "GPUDSD=X", "multiplier": random.random() * random.randint(1, 10)}],
    "negative": [], 
    "aggregation":  "sum", 
    "priceType": "absolute", 
    "thresholdType": "level", 
    "threshold": random.random(), 
    "triggerType": "filter", 
    "triggerBias": "above"
}], 
"combination": 1
}
with open("sampleLong.json", "w") as outfile:
    json.dump(my_dic_long, outfile)