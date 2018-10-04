# This Python file uses the following encoding: utf-8

import pandas as pd
import os

import connect_to_twitter
from library import print_err

def get(screen_name, max_results=100):
    api = connect_to_twitter.api()

    faved_tweets = pd.DataFrame()
    collecting_is_done = False
    results_count = 0
    last_id = None

    while (collecting_is_done is False):
        print('Getting favorites for', screen_name)
        try:
            favorites = api.GetFavorites(screen_name=screen_name, count=max_results, max_id=last_id)
            faved_tweets_batch = []
            for favorite in favorites:
                faved_tweets_batch.append([screen_name,
                                           favorite.user.screen_name,
                                           favorite.text,
                                           favorite.id,
                                           favorite.created_at])
            faved_tweets = faved_tweets.append(
                pd.DataFrame(faved_tweets_batch, columns=['from','to','text', 'id', 'created_at']),
                ignore_index=True
            )

            print('Found', len(favorites))
            results_count += len(favorites)
            if (results_count >= max_results) or len(favorites) <= 1:
                collecting_is_done = True
            else:
                last_id = favorites[-1].id
        except Exception as e:
            print_err(e)
            collecting_is_done = True

    return faved_tweets


def append_to_csv(screen_name, file_name, max_results):
    faves = get(screen_name, max_results)

    if os.path.exists(file_name):
        print('Appending to existing', file_name)
        with open(file_name, 'a') as csv_file:
            faves.to_csv(csv_file, index=False, encoding='utf8', header=False)
    else:
        faves.to_csv(file_name, index=False, encoding='utf8')
