'''
    for long in longs:
        risk_management = long.risk_management
        merge_data = pd.read_csv(PATH.format(long.ticker))
        columns = list(merge_data.columns)
        cols = list(set(WANTED_PRICES) & set(columns))
        if not "Close" in columns:
            raise Exception(long.ticker + " does not have close price")
        else:
            source_data[CLOSE.format(long.ticker)] = ""
        if "Open" in columns:
            source_data[OPEN.format(long.ticker)] = ""
        if "High" in columns:
            source_data[HIGH.format(long.ticker)] = ""
        elif risk_management.order == "OCO":
            raise Exception(long.ticker + " cannot have long OCO order without high")
        if "Low" in columns:
            source_data[LOW.format(long.ticker)] = ""
        elif risk_management.order != "MOC":
            raise Exception(long.ticker + " cannot have long non-MOC order without low")
        for ind, row in merge_data.iterrows():    
            for col in cols:
                source_data.loc[source_data.date == row["Date"], long.ticker + "_" + col] = row[col]
    print(source_data)

    for short in shorts:
        risk_management = short.risk_management
        merge_data = pd.read_csv(PATH.format(short.ticker))
        columns = list(merge_data.columns)
        cols = list(set(WANTED_PRICES) & set(columns))
        if not "Close" in columns:
            raise Exception(short.ticker + " does not have close price")
        else:
            source_data[CLOSE.format(short.ticker)] = ""
        if "Open" in columns:
            source_data[OPEN.format(short.ticker)] = ""
        if "High" in columns:
            source_data[HIGH.format(short.ticker)] = ""
        elif risk_management.order != "MOC":
            raise Exception(short.ticker + " cannot have short non-MOC order without high")
        if "Low" in columns:
            source_data[LOW.format(short.ticker)] = ""
        elif risk_management.order == "OCO":
            raise Exception(short.ticker + " cannot have short OCO order without low")
        for ind, row in merge_data.iterrows():    
            for col in cols:
                source_data.loc[source_data.date == row["Date"], short.ticker + "_" + col] = row[col]
    '''