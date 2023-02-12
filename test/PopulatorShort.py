import json
import random
my_dic_short = {}
my_dic_short["lookback"] = {"startDate": "06-12-2019", "endDate": "07-15-2019", "step": random.randint(0, 1440)}
my_dic_short["tradeStructure"] = {"long": [], 
    "short": [{"ticker": "EURUSD=X", "execution": "market", "riskManagement": {
    "order": "OCO", 
     "takeProfit": -random.random()*2, 
     "stopLoss": random.random()*2, 
     "marketOnClose": random.randint(1, 20)
    }}]
}
my_dic_short["signals"] = { 
    "indicators" : [{
    "positive": [{"symbol": "GPUDSD=X", "multiplier": random.random() * random.randint(1, 10)}],
    "negative": [], 
    "aggregation":  "average", 
    "priceType": "absolute", 
    "thresholdType": "level", 
    "threshold": random.random(), 
    "triggerType": "filter", 
    "triggerBias": "above"
}], 
"combination": 1
}
with open("sampleShort.json", "w") as outfile:
    json.dump(my_dic_short, outfile)