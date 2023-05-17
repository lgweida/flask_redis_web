import time

#import redis
from flask import Flask, request
import json
import pandas as pd
from finvizfinance.quote import finvizfinance, Quote
from finvizfinance.quote import Quote
from finvizfinance.earnings import Earnings
from json import loads, dumps

stock = finvizfinance('tsla')
quote = Quote()
q = quote.get_current("tsla");


app = Flask(__name__)
#cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            #return cache.incr('hits')
            return 100
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times. {}\n'.format(count, q)

@app.route('/earnings')
def earnings():
    earnings = Earnings()
    
    return earnings.to_json()
    
@app.route('/insider', methods=['GET'])
def insider():
    args = request.args
    ticker = args.get('ticker')
    stock = finvizfinance(ticker)
    inside_trader_df = stock.ticker_inside_trader()
    json_str = inside_trader_df.to_json(orient='records', lines=False)
    json_rec=loads(json_str)
    return  dumps(json_rec)

@app.route('/quote', methods=['GET'])
def get_quote():
    args = request.args
    ticker = args.get('ticker')
    q = quote.get_current(ticker);
    my_quote ={"ticker": ticker,
               "price" : q
              }
     
    
    return dumps(my_quote)

@app.route('/calendar', methods=['GET'])
def calendar():
    cal_df = finvizfinance.calendar.Calendar().calendar()
    json_str = cal_df.to_json(orient='records', lines=False)
    json_rec=loads(json_str)
    return  dumps(json_rec)
#finvizfinance.calendar.Calendar
