# This Python file uses the following encoding: utf-8

import twitter
# import unicodecsv as csv
import re
import os
import argparse

import connect_to_twitter

parser = argparse.ArgumentParser(description='Given a Twitter list, collect liked tweets and retweets, and the profiles of the tweeters')
parser.add_argument('--list', dest='list', help='Slug of the Twitter list', required=True)
parser.add_argument('--owner', dest='owner_screen_name', help='Screen name of the Twitter list', required=True)
args = parser.parse_args()


api = connect_to_twitter.api()

list_members = api.GetListMembers(slug=args.list, owner_screen_name=args.owner_screen_name)

exit()


# mps_latest_fave_status_ids = {}
# mps_latest_retweet_status_ids = {}
#
# if os.path.isfile('faves.csv'):
#     print('Found existing faves.csv')
#     previous_user = None
#     with open('faves.csv', 'r') as faves_csv:
#         for row in csv.reader(faves_csv):
#             current_user = row[0]
#             if current_user != previous_user:
#                 previous_user = current_user
#                 mps_latest_fave_status_ids[current_user] = row[2]
#
# if os.path.isfile('retweets.csv'):
#     print('Found existing retweets.csv')
#     previous_user = None
#     with open('retweets.csv', 'r') as retweets_csv:
#         for row in csv.reader(retweets_csv):
#             current_user = row[0]
#             if current_user != previous_user:
#                 previous_user = current_user
#                 mps_latest_retweet_status_ids[current_user] = row[2]

faved_screennames = set()

with open('faves.csv', 'a') as faves_csv:
    writer = csv.writer(faves_csv)
    if not os.path.isfile('faves.csv'):
        writer.writerow(['from', 'to', 'id', 'text', 'from_screenname', 'to_screenname'])

    for mp in mps:
        since_id = None
        if mp.name in mps_latest_fave_status_ids:
            since_id = mps_latest_fave_status_ids[mp.name]
            print('Looking for tweets for', mp.name, 'after', since_id)
        favorites = api.GetFavorites(user_id=mp.id, since_id=since_id)

        for favorite in favorites:
            print(mp.name, '❤️ ', favorite.user.name, favorite.created_at)
            writer.writerow([mp.name, favorite.user.name, favorite.id, favorite.text, mp.screen_name, favorite.user.screen_name])
            faved_screennames.add(favorite.user.screen_name)

with open('retweets.csv', 'a') as retweet_csv:
    writer = csv.writer(retweet_csv)
    if not os.path.isfile('retweets.csv'):
        writer.writerow(['from', 'to', 'id', 'text', 'from_screenname', 'to_screenname'])

    for mp in mps:
        since_id = None
        if mp.name in mps_latest_retweet_status_ids:
            since_id = mps_latest_retweet_status_ids[mp.name]
            print('Looking for unquoted retweets by', mp.name, 'after', since_id)
        tweets = api.GetUserTimeline(user_id=mp.id, since_id=since_id, include_rts=True, exclude_replies=True, trim_user=False)

        for tweet in tweets:
            try:
                retweet = tweet.retweeted_status
                if not tweet.quoted_status_id:
                    print(mp.name, 'RT', retweet.user.name, retweet.created_at)
                    writer.writerow([mp.name, retweet.user.name, retweet.id, retweet.text, mp.screen_name, retweet.user.screen_name])
                    faved_screennames.add(retweet.user.screen_name)
            except:
                1

print("Looking & and recording people found")

with open('people.csv', 'a') as people_csv:
    writer = csv.writer(people_csv)
    if not os.path.isfile('people.csv'):
        writer.writerow(['label', 'type', 'description', 'screen_name', 'image'])

    for screen_name in faved_screennames:
        # TODO: check whether user is already in people.csv, and skip if so
        user = api.GetUser(screen_name=screen_name)
        row = user.name, '', user.description, user.screen_name, user.profile_image_url
        writer.writerow(row)

print("New tweets collected:", len(faved_screennames))
