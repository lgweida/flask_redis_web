import time

#import redis
from flask import Flask, request
import json
import pandas as pd
from finvizfinance.quote import finvizfinance, Quote
from finvizfinance.quote import Quote
from finvizfinance.calendar import Calendar
from json import loads, dumps
from finvizfinance.earnings import Earnings

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
    fEarnings = Earnings()
    df_days = fEarnings.partition_days(mode='financial')
    return df_days.to_json()
    
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
    response = app.response_class(
        response=dumps(my_quote),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/calendar', methods=['GET'])
def calendar():
    fcalendar = Calendar()
    df = fcalendar.calendar()
    json_str = df.to_json(orient='records', lines=False)
    json_rec=loads(json_str)
    
    return  dumps(json_rec)
#finvizfinance.calendar.Calendar
