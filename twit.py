# This Python file uses the following encoding: utf-8

from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env', verbose=True)

import twitter
import unicodecsv as csv
import re
import os

def get_type(description):
    type = ''
    if re.search(r'\blabour\b', description, re.IGNORECASE):
        type = 'Labour'
    elif re.search(r'\bgreen|17 garrett\b', description, re.IGNORECASE):
        type = 'Green'
    elif re.search(r'\bnational\b', description, re.IGNORECASE):
        type = 'National'
    elif re.search(r'\bnew zealand first|nz first|nz_first\b', description, re.IGNORECASE):
        type = 'New Zealand First'
    elif re.search(r'\bact\b', description, re.IGNORECASE):
        type = 'ACT'
    return type

print 'Connecting to Twitter… (pauses to stay under rate limit)'
api = twitter.Api(consumer_key=os.getenv('consumer_key'),
                  consumer_secret=os.getenv('consumer_secret'),
                  access_token_key=os.getenv('access_token_key'),
                  access_token_secret=os.getenv('access_token_secret'),
                  sleep_on_rate_limit=True)

mps = api.GetListMembers(slug='mps', owner_screen_name='NZParliament')

mps_latest_fave_status_ids = {}

if os.path.isfile('faves.csv'):
    print 'Found existing faves.csv'
    previous_user = None
    with open('faves.csv', 'r') as faves_csv:
        for row in csv.reader(faves_csv):
            current_user = row[0]
            if current_user != previous_user:
                previous_user = current_user
                mps_latest_fave_status_ids[current_user] = row[2]

faved_screennames = set()

with open('faves.csv', 'a') as faves_csv:
    writer = csv.writer(faves_csv)
    if not os.path.isfile('faves.csv'):
        writer.writerow(['from', 'to', 'id', 'text'])

    for mp in mps:
        since_id = None
        if mp.name in mps_latest_fave_status_ids:
            since_id = mps_latest_fave_status_ids[mp.name]
            print 'Looking for tweets for', mp.name, 'after', since_id
        favorites = api.GetFavorites(user_id=mp.id, since_id=since_id)

        for favorite in favorites:
            print mp.name, '❤️ ', favorite.user.name, favorite.created_at, favorite.text
            writer.writerow([mp.name, favorite.user.name, favorite.id, favorite.text])
            faved_screennames.add(favorite.user.screen_name)

with open('people.csv', 'a') as people_csv:
    writer = csv.writer(people_csv)
    if not os.path.isfile('people.csv'):
        writer.writerow(['label', 'type', 'description', 'screen_name', 'image'])

    for screen_name in faved_screennames:
        # TODO: check whether they're in the MPs list, for setting the type more accurately
        user = api.GetUser(screen_name=screen_name)
        row = user.name, get_type(user.description), user.description, user.screen_name, user.profile_image_url
        print row
        writer.writerow(row)

print "New tweets collected:", len(faved_screennames)
