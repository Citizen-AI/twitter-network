from requests import request
import pandas as pd
import re

from library import pd_to_csv


def cluster(ids, text):
    data = "key=6f930f604340a90098eec6be9e7b2af1&lang=en&mode=dg&txt=" + text + "&id=" + ids
    response = request("POST", 'https://api.meaningcloud.com/clustering-1.1',
                   data=data.encode('utf-8'),
                   headers={'content-type': 'application/x-www-form-urlencoded'})
    return response.text


def concat_tweets():
    def strip_join(text):
        return ' '.join(text).replace('\n', '')

    print('Concatenating liked tweets')
    faves = pd.read_csv('output/mps-faves.csv')
    people = faves.pivot_table(index=['from'], values=['text'], aggfunc=strip_join)
    people.reset_index(level=['from'], inplace=True)
    print('Exporting to csv')
    pd_to_csv(people, 'mps-people-concat-tweets.csv')


def people_cluster():
    people = pd.read_csv('output/mps-people-concat-tweets.csv')
    ids = people.to_string(columns=['from'], index=False, header=False)
    text = people.to_string(columns=['text'], index=False, header=False)

    print(ids.count('\n'))
    print(text.count('\n'))
    # print(cluster(ids, text))


people_cluster()
