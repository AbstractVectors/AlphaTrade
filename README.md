# Backtester
This is a sample of our user input, which is then read by our codebase. From there, the trades are measured over time. Graphs are outputted at the end. 



```yaml

{
    // Specifies the lookup period of the backtest
    // startDate and endDate should be entered in the form mm-dd-yyyy
    // step is the time interval, in minutes, between checks. Supply an int
    "lookback": {
        "startDate": "mm-dd-yyyy",
        "endDate": "mm-dd-yyyy",
        "step": "int"
    },
    // Specifies the trade expression that will be tested
    // In long and short, place a list of objects of all securities that will be bought or sold short
    // For the ticker, please use "=X" for forex pairs, "=F" for commodities, and "" for stocks and fixed income
    // execution can be market or limit (NOTE-> we currently only support market)
    // Within risk management, order can be OCO (one cancels other), SLMOC (stop loss + market on close), MOC (market on close)
        // For OCO, enter an float for takeProfit and stopLoss, while leaving marketOnClose blank
        // For SLMOC, enter an float for stopLoss and a date in the form mm-dd-yyyy for marketOnClose, while leaving takeProfit blank
        // For MOC, enter a date in the form mm-dd-yyyy for marketOnClose, while leaving takeProfit and stopLoss blank
    "tradeStructure": {
        "long": [
            {
                "ticker": "str",
                "execution": "str",
                "riskManagement": {
                    "order": "str",
                    "takeProfit": "float",
                    "stopLoss": "float",
                    "marketOnClose": "int"
                }
            }, 
            {}
        ],
        "short": [
            {
                "ticker": "str",
                "execution": "str",
                "riskManagement": {
                    "order": "str",
                    "takeProfit": "float",
                    "stopLoss": "float",
                    "marketOnClose": "int"
                }
            },
            {}
        ]
    },
    // Specifies the indicators that will be used as triggers for buy/sell
    // In indicators, provide a list of indicators that will be used
        // For each indicator, provide a list of data that are positive and negative (e.g. if you wanted to track US10y and JGB10y yield differential on an FX-hedged basis, US10y would be positive and JGB10y & FX-hedging costs would be negative)
            // For each datapoint:
                // symbol will be the symbol of the indicator/ticker of the security
                // multiplier will be the multiplier that will be applied to the datapoint (NOTE-> if you want all of the indicators to be vol adjusted, leave it blank)
        // aggregation can be sum or average
        // priceType can be absolute or percent
        // thresholdType can be level or zscore
        // threshold is a floating point number
        // triggerType can be filter or break
        // triggerBias can be above or below (e.g. 
            // if you're tracking NYMEX crude vs USDCAD:
                // you can use a filter for the 1 week deviation between crude and USDCAD. Any time the deviation is above x-sigma, this will trigger a buy/sell
                // you can use a break for the 1 week deviation between crude and USDCAD. If the deviation breaks above x-sigma, this will trigger a buy/sell)
        // timeFilterUnit can be minute, hour, day, week, month, etc
        // timeFilter takes values of time that will be considered for the signal (positive numbers used for time from first element of interval, negative numbers used for time from last element of interval)
    // combination is the minimum number of indicators needed to trigger a signal
    "signals": {
        "indicators": [
            {
                "positive": [
                    {
                        "symbol": "str",
                        "multiplier": "float"
                    },
                    {}
                ],
                "negative": [
                    {
                        "symbol": "str",
                        "multiplier": "float"
                    },
                    {}
                ],
                "aggregation": "str",
                "priceType": "str",
                "thresholdType": "str",
                "threshold": "float",
                "triggerType": "str",
                "triggerBias": "str",
                "timeFilterUnit": "str",
                "timeFilter": "list"
            },
            {}
        ],
        "combination": "int"
    }
}

```







