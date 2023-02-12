import random 
import datetime
def random_date_generator(start_time, end_date):
    random_number_of_days = random.randrange((end_date - start_date).days)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date
ticker = ["EURUSD=X", "CPI XYOY Index", "CSA1 Comdty", "DGS10", "GJGB10", "GBPUSD", "JPY10Y", 
        "LHA Comdty", "NOSMFSVL", "NZDUSD=X"]
start_date = random_date_generator(datetime.date(2015, 1, 1), datetime.date(2022, 12, 4))
end_date = random_date_generator()
long = {}
