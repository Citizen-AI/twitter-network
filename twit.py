# This Python file uses the following encoding: utf-8

from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env', verbose=True)

from pprint import pprint
import twitter
import unicodecsv as csv
import re
import os

api = twitter.Api(consumer_key=os.getenv("consumer_key"),
                  consumer_secret=os.getenv("consumer_secret"),
                  access_token_key=os.getenv("access_token_key"),
                  access_token_secret=os.getenv("access_token_secret"),
                  sleep_on_rate_limit=True)

mps = api.GetListMembers(slug="mps", owner_screen_name="NZParliament")

with open('mps.csv', 'wb') as mps_csvfile:
    writer = csv.writer(mps_csvfile)
    writer.writerow(["label", "type", "image"])
    for mp in mps:
        favorites = api.GetFavorites(user_id = mp.id)
        party = "MP"
        if re.search("labour", mp.description, re.IGNORECASE):
            party = "Labour"
        elif re.search("green", mp.description, re.IGNORECASE):
            party = "Green"
        elif re.search("national", mp.description, re.IGNORECASE):
            party = "National"
        elif re.search("new zealand first|nz first|nz_first", mp.description, re.IGNORECASE):
            party = "New Zealand First"
        elif re.search("act", mp.description, re.IGNORECASE):
            party = "ACT"

        row = mp.name, party, mp.profile_image_url
        print row
        writer.writerow(row)

with open('faves.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["from", "to"])

    for mp in mps:
        # statuses = api.GetUserTimeline(user_id=mps[0].id, exclude_replies=True)
        # for status in statuses:
        #     if status.retweeted_status:
        #         print mp.name, "RT ", status.retweeted_status.user.name
        #         writer.writerow([mp.name, status.retweeted_status.user.name])

        favorites = api.GetFavorites(user_id = mp.id)
        for favorite in favorites:
            print mp.name, "❤️ ", favorite.user.name
            writer.writerow([mp.name, favorite.user.name])
