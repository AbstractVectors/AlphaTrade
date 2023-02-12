import json
import pandas
import pymongo

CLIENT_ID = 'mongodb+srv://anyone:xyz@flask.ngjrl.mongodb.net/Volidity?retryWrites=true&w=majority'
DB_ID = 'Volidity'
COL_ID = 'data'

def push_data(ticker: str, df: pandas.DataFrame):
    client = pymongo.MongoClient(CLIENT_ID)
    db = client[DB_ID]
    col = db[COL_ID]
    decoder = json.JSONDecoder()
    col.insert_one({'ticker': ticker, 'data': decoder.decode(df.to_json())})
    client.close()

def pull_data(ticker: str):
    client = pymongo.MongoClient(CLIENT_ID)
    db = client[DB_ID]
    col = db[COL_ID]
    document = dict(col.find_one({'ticker': ticker}))
    encoder = json.JSONEncoder()
    return pandas.read_json(encoder.encode(document['data']))


