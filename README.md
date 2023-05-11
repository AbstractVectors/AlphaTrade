<h1>Backtester Server</h1>
<hr>
<strong>View Deployment: <a href="https://alphatrade.herokuapp.com/">https://alphatrade.herokuapp.com/</a></strong>
<hr>
<h2>Server Breakdown</h2>
<table>
    <tr>
        <th>Title</th>
        <th>HTML File</th>
        <th>Python Function</th>
        <th>Route</th>
        <th>Visibility</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>Home</td>
        <td>home.html</td>
        <td>home()</td>
        <td>/</td>
        <td>public</td>
        <td>Home page for landing HTTP requests.</td>
    </tr>
    <tr>
        <td>Login</td>
        <td>login.html</td>
        <td>login()</td>
        <td>/login</td>
        <td>public</td>
        <td>Login page for users.</td>
    </tr>
    <tr>
        <td>Registration</td>
        <td>registration.html</td>
        <td>registration()</td>
        <td>/registration</td>
        <td>public</td>
        <td>Account creation.</td>
    </tr>
    <tr>
        <td>Financial Strategy Dashboard</td>
        <td>dashboard.html</td>
        <td>dashboard()</td>
        <td>/dashboard</td>
        <td>private</td>
        <td>Page for viewing previously saved financial strategies and creating new strategies.</td>
    </tr>
    <tr>
        <td>View</td>
        <td>view.html</td>
        <td>view()</td>
        <td>/view</td>
        <td>private</td>
        <td>Viewing analysis results.</td>
    </tr>
    <tr>
        <td>Parameter View and Edit</td>
        <td>params.html</td>
        <td>params()</td>
        <td>/params</td>
        <td>private</td>
        <td>Viewing and editing parameters for saving previously saved strategies.</td>
    </tr>
</table>
<hr>
<h2>Database Structure</h2>
<strong>Volidity Database</strong>
<ol>
<li>data collection for storing financial data.</li>
    <ol>
        <li>id: unique identifier</li>
        <li>ticker: stock symbol</li>
        <li>data: pandas DF with stock data</li>
        <li>user: user to whom the data pertains</li>
    </ol>
<li>user collection for storing login/registration information</li>
    <ol>
        <li>id: unique identifier</li>
        <li>username: unique username for users to login</li>
        <li>password: password for unlocking user account</li>
        <li>name: name of user</li>
    </ol>
<li>strategy collection</li>
    <ol>
        <li>id: unique identifier</li>
        <li>ticker: stock symbol</li>
        <li>param1</li>
        <li>...</li>
        <li>paramn</li>
    </ol>
</ol>

Graphs:
1)  PnL vs Time (Date, X amount of labels), Linegraph
2)  Cumsum vs Time 
3)  Signals vs Time, Linegraph
4)  Histogram of daily % returns
5)  Time vs SD (if we have time), optional

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
