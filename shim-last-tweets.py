# This Python file uses the following encoding: utf-8

from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env', verbose=True)

import twitter
import pandas
import os

print 'Connecting to Twitter…'
api = twitter.Api(consumer_key=os.getenv('consumer_key'),
                  consumer_secret=os.getenv('consumer_secret'),
                  access_token_key=os.getenv('access_token_key'),
                  access_token_secret=os.getenv('access_token_secret'),
                  sleep_on_rate_limit=False)

faves = pandas.read_csv('faves.csv')

faves_lacking_text = faves.loc[faves['text'].isnull()]

statuses = api.GetStatuses(status_ids=faves_lacking_text['id'], trim_user=True, include_entities=False)

for status in statuses:
    try:
        faves.loc[faves['id'] == status.id, 'text'] = status.text
    except:
        print "some error with", status.id, status.text

faves.to_csv('missing-statuses.csv', encoding='utf-8', index=False)
