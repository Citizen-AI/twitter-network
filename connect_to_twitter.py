# This Python file uses the following encoding: utf-8

import twitter
import os

def api():
    print('Connecting to Twitter… (sleeps to avoid rate limiting)')
    return twitter.Api(consumer_key=os.getenv('consumer_key'),
                      consumer_secret=os.getenv('consumer_secret'),
                      access_token_key=os.getenv('access_token_key'),
                      access_token_secret=os.getenv('access_token_secret'),
                      sleep_on_rate_limit=True)
