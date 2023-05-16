import time

#import redis
from flask import Flask
import json
import pandas as pd
from finvizfinance.quote import finvizfinance
from finvizfinance.quote import Quote

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
    return 'Hello World! I have been seen {} times. {}\n'.format(count, "hello World")
    
   
