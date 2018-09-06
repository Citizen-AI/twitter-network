# This Python file uses the following encoding: utf-8

from collections import Counter
import pandas as pd
from gspread_dataframe import set_with_dataframe

import connect_to_twitter
import connect_to_google_sheets
from library import wordcount, print_err


def collect_users_faves(screen_name):
    api = connect_to_twitter.api()

    faved_tweets = pd.DataFrame()
    collecting_is_done = False
    max_results = 100
    results_count = 0
    last_id = None

    while (collecting_is_done is False):
        print('Getting favorites for', screen_name)
        try:
            favorites = api.GetFavorites(screen_name=screen_name, count=200, max_id=last_id)
            faved_tweets_batch = []
            for favorite in favorites:
                faved_tweets_batch.append([screen_name, favorite.user.screen_name, favorite.text])
            faved_tweets = faved_tweets.append(pd.DataFrame(faved_tweets_batch, columns=['from','to','text']), ignore_index=True)

            print('Found', len(favorites))
            results_count += len(favorites)
            if (results_count >= max_results) or len(favorites) <= 1:
                collecting_is_done = True
            else:
                last_id = favorites[-1].id
        except Exception as e: print_err(e)

    return faved_tweets


def column_contains_value(df, col, val):
    return len(df[df[col].str.match(val)]) is not 0

# networks_faves = l1_users_faves = collect_users_faves('mhjb')
# for index in l1_users_faves.index:
#     user = l1_users_faves.at[index,'to']
#     if not column_contains_value(networks_faves, 'from', user):
#         networks_faves = networks_faves.append(collect_users_faves(user))
#
# print 'Writing to CSV'
# networks_faves.to_csv('network.csv', index=False, encoding='utf8')

# TODO: Can we get more of long tweets?

def people_from_network():
    network = pd.read_csv('network.csv')
    print('Adding up multiple tweets favorited by & from the same people')
    network = network.pivot_table(index=['from','to'], values=['text'], aggfunc={'to':'count','text':'last'})
    network.columns=['last_text','times']
    network.reset_index(level=['from','to'], inplace=True)

    print('Counting up number of times each person favourited and word frequencies')

    def word_freq(series):
       combined_text = reduce(lambda x, y: x + ' ' + y, series)
       freq_table = wordcount(combined_text, 10)
       return ' '.join(zip(*freq_table)[0])

    people = network.pivot_table(index=['to'], values=['from','last_text'], aggfunc={'from':'count','last_text':word_freq})
    people.reset_index(level=['to'], inplace=True)
    people.columns = ['label','favees','liked_tweets_words']

    # popular_people = people.loc[people['favees']>1]

    print('Writing to CSV')
    people.to_csv('people-in-network.csv', index=False, encoding='utf8')


def populate_people_profiles():
    api = connect_to_twitter.api()

    people = pd.read_csv('people-in-network.csv')

    print('Looking up user profiles…')
    for index in people.index:
        screen_name = people.at[index,'label']
        print(screen_name, end=', ', flush=True)
        try:
            user = api.GetUser(screen_name=screen_name)
        except Exception as e: print_err(e)
        # TODO: use UsersLookup to get 100 users at a time https://python-twitter.readthedocs.io/en/latest/twitter.html#twitter.models.User

        people.at[index,'name'] = user.name
        people.at[index,'description'] = user.description
        people.at[index,'image'] = user.profile_image_url

        # if index > 10: break

    print('Writing new CSV')
    people.to_csv('people-in-network-with-profiles.csv', index=False, encoding='utf8')


def upload():
    sheets = connect_to_google_sheets.sheets()
    print('Reading CSVs')
    network = pd.read_csv('network.csv')
    people = pd.read_csv('people-in-network-with-profiles.csv')

    confirm = input('OK to delete & replace worksheets? (Y/n) ')
    if confirm is '' or strtobool(confirm):
        print('Deleting')
        try: # currently needs one useless worksheet hanging about (can't delete all sheets)
            sheets.del_worksheet(sheets.worksheet('network'))
            sheets.del_worksheet(sheets.worksheet('people'))
        except Exception as e: print_err(e)

        print('Creating new worksheets')
        faves_worksheet = sheets.add_worksheet(title='network', rows=network.shape[0], cols=network.shape[1])
        people_worksheet = sheets.add_worksheet(title='people', rows=people.shape[0], cols=people.shape[1])
        print('Uploading network')
        set_with_dataframe(faves_worksheet, network)
        print('Uploading people')
        set_with_dataframe(people_worksheet, people)

upload()
# https://docs.google.com/spreadsheets/d/17GaTkdVFB7iqDvcaLbBEomVQtgK_p0BhXXinSxNsXn0/edit#gid=404698243
