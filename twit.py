# This Python file uses the following encoding: utf-8

from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env', verbose=True)

from pprint import pprint
import twitter
import unicodecsv as csv
import re
import os

def get_party(description):
    party = "MP"
    if re.search("labour", description, re.IGNORECASE):
        party = "Labour"
    elif re.search("green", description, re.IGNORECASE):
        party = "Green"
    elif re.search("national", description, re.IGNORECASE):
        party = "National"
    elif re.search("new zealand first|nz first|nz_first", description, re.IGNORECASE):
        party = "New Zealand First"
    elif re.search("act", description, re.IGNORECASE):
        party = "ACT"
    return party

print "Connecting to Twitter… (pauses to stay under rate limit)"
api = twitter.Api(consumer_key=os.getenv("consumer_key"),
                  consumer_secret=os.getenv("consumer_secret"),
                  access_token_key=os.getenv("access_token_key"),
                  access_token_secret=os.getenv("access_token_secret"),
                  sleep_on_rate_limit=True)

mps = api.GetListMembers(slug="mps", owner_screen_name="NZParliament")

with open('mps.csv', 'wb') as mps_csvfile:
    writer = csv.writer(mps_csvfile)
    writer.writerow(["label", "type", "description", "image"])
    for mp in mps:
        row = mp.name, get_party(mp.description), mp.description, mp.profile_image_url
        print row
        writer.writerow(row)

with open('faves.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["from", "to"])

    for mp in mps:
        favorites = api.GetFavorites(user_id = mp.id)
        for favorite in favorites:
            print mp.name, "❤️ ", favorite.user.name
            writer.writerow([mp.name, favorite.user.name])
