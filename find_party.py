"""Example of Python client calling Knowledge Graph Search API."""
import json
from urllib.parse import urlencode
from urllib.request import urlopen
import os
from pprint import pprint
import re


api_key = os.getenv('google_api_key')
# pp = pprint.PrettyPrinter(indent=2)


def knowledge_graph_get(query):
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 10,
        'indent': True,
        'key': api_key,
    }
    url = service_url + '?' + urlencode(params)
    with urlopen(url) as response:
        data = json.loads(response.read())
        try:
            return data['itemListElement'][0]['result']['detailedDescription']['articleBody']
        except:
            return ''


def search(str, country='us'):
    output = None
    try:
        if country is 'us':
            if re.search('Independent', str, re.IGNORECASE):
                output = 'Republican'
            elif re.search('Republican', str):
                output = 'Republican'
            elif re.search('Democrat', str):
                output = 'Democrat'
        elif country is 'nz':
            if re.search('National', str):
                output = 'National'
            elif re.search('Labour', str):
                output = 'Labour'
            elif re.search('NZ First|New Zealand First', str):
                output = 'NZ First'
            elif re.search('Green', str):
                output = 'Green'
            elif re.search('Act', str):
                output = 'Act'

    except: pass
    return output


def knowledge_graph_get_party(person, country):
    kg_details = knowledge_graph_get(person)
    pprint(kg_details)
    return search(kg_details, country)
