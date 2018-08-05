# This Python file uses the following encoding: utf-8

from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env', verbose=True)

import twitter
import os
from collections import Counter
import pandas as pd

print 'Connecting to Twitter… (sleeps to avoid rate limiting)'
api = twitter.Api(consumer_key=os.getenv('consumer_key'),
                  consumer_secret=os.getenv('consumer_secret'),
                  access_token_key=os.getenv('access_token_key'),
                  access_token_secret=os.getenv('access_token_secret'),
                  sleep_on_rate_limit=True)

def collect_users_faves(screen_name):
    faved_screennames = Counter()
    collecting_is_done = False
    max_results = 100
    results_count = 0
    last_id = None

    while (collecting_is_done is False):
        print 'Getting favorites for', screen_name
        try:
            favorites = api.GetFavorites(screen_name=screen_name, count=200, max_id=last_id)
            # print favorites
            for favorite in favorites:
                faved_screennames[favorite.user.screen_name] += 1

            print 'Found', len(favorites)
            results_count += len(favorites)
            if (results_count >= max_results) or len(favorites) <= 1: collecting_is_done = True

            last_id = favorites[-1].id
        except Exception as e: print e

    return faved_screennames


def counter_to_pd(counter):
    df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
    df.rename(columns={'index':'to', 0:'count'}, inplace=True)
    return df


l1_users = counter_to_pd(collect_users_faves('mhjb'))
l1_users['from'] = 'mhjb'

network = l1_users

for index in l1_users.index:
    user = l1_users.at[index,'to']
    l2_users = counter_to_pd(collect_users_faves(user))
    l2_users['from'] = user
    network = network.append(l2_users)

    # if index is 25: break

network = network[['from','to','count']]
print 'Writing to CSV'
network.to_csv('network.csv', index=False)
