# This Python file uses the following encoding: utf-8

from collections import Counter
import pandas as pd
import os
from pprint import pprint
import json

import connect_to_twitter
from library import wordcount, print_err, column_contains_value, csv_to_gsheet
import user_faves
import find_party


OUTPUT_FOLDER = 'output/'


def list_faves_to_csv(slug, owner_screen_name, csv):
    api = connect_to_twitter.api()
    list_members = api.GetListMembers(slug=slug, owner_screen_name=owner_screen_name)
    for list_member in list_members:
        user_faves.append_to_csv(list_member.screen_name, OUTPUT_FOLDER + csv)


def list_to_csv(slug, owner_screen_name, csv):
    api = connect_to_twitter.api()
    list_members = api.GetListMembers(slug=slug, owner_screen_name=owner_screen_name)
    list_members_df = pd.DataFrame()
    for person in list_members:
        data = {'label':person.screen_name, 'name':person.name, 'description':person.description}
        list_members_df = list_members_df.append(data, ignore_index=True)
    list_members_df.to_csv(OUTPUT_FOLDER + csv, index=False, encoding='utf8')


def faves_to_network(faves_csv, network_csv):
    faves = pd.read_csv(OUTPUT_FOLDER + faves_csv)
    print('Adding up multiple tweets favorited by & from the same people')
    network = faves.pivot_table(index=['from','to'], values=['text'], aggfunc={'to':'count','text':'last'})
    network.columns=['last_text','times']
    network.reset_index(level=['from','to'], inplace=True)
    print('Writing to', network_csv)
    network.to_csv(OUTPUT_FOLDER + network_csv, index=False, encoding='utf8')


def network_to_people(network_csv, people_csv):
    network = pd.read_csv(OUTPUT_FOLDER + network_csv)
    people = network.pivot_table(index=['to'], values=['from','last_text'], aggfunc={'from':'count'})
    people.reset_index(level=['to'], inplace=True)
    people.columns = ['label','favees']
    print('Writing to', people_csv)
    people.to_csv(OUTPUT_FOLDER + people_csv, index=False, encoding='utf8')


def remove_unpopular_people(people_csv, network_csv, minimum_favees=1):
    people = pd.read_csv(OUTPUT_FOLDER + people_csv)
    network = pd.read_csv(OUTPUT_FOLDER + network_csv)
    popular_people = people.loc[people['favees'] >= minimum_favees]
    network = network.loc[network['to'].isin(popular_people['label'])]
    popular_people.to_csv(OUTPUT_FOLDER + people_csv, index=False, encoding='utf8')
    network.to_csv(OUTPUT_FOLDER + network_csv, index=False, encoding='utf8')


def populate_profiles(people_csv):
    people = pd.read_csv(OUTPUT_FOLDER + people_csv)
    api = connect_to_twitter.api()

    print('Looking up user profiles…')
    for index in people.index:
        screen_name = people.at[index, 'label']
        print(screen_name, end=', ', flush=True)
        try: user = api.GetUser(screen_name=screen_name)
        except Exception as e: print_err(e)
        # TODO: use UsersLookup to get 100 users at a time https://python-twitter.readthedocs.io/en/latest/twitter.html#twitter.models.User

        people.at[index,'name'] = user.name
        people.at[index,'description'] = user.description
        people.at[index,'image'] = user.profile_image_url

    print('Updating', people_csv)
    people.to_csv(OUTPUT_FOLDER + people_csv, index=False, encoding='utf8')


def add_party_to_list(list_csv):
    """Looks for US political party affiliation"""
    list = pd.read_csv(list_csv)
    for index in list.index:
        name = list.at[index, 'name']
        description = list.at[index, 'description']
        party = find_party.search(description) or find_party.search(name) or find_party.knowledge_graph_get_party(name)
        print(name, ',', party)
        if party:
            list.at[index, 'party'] = party
    list.to_csv(list_csv, index=False, encoding='utf8')


def merge_people(csv1, csv2, output_csv):
    df1 = pd.read_csv(OUTPUT_FOLDER + csv1)
    df2 = pd.read_csv(OUTPUT_FOLDER + csv2)
    merged = pd.merge(df1, df2, on=['label','name','description'], how='outer')
    merged.to_csv(OUTPUT_FOLDER + output_csv, index=False, encoding='utf8')


def csvs_to_3d_force_graph_json(nodes_csv, links_csv, output_json):
    nodes_df = pd.read_csv(OUTPUT_FOLDER + nodes_csv, keep_default_na=False)
    nodes_df.rename(columns={'label':'id', 'favees':'val'}, inplace=True)
    nodes = nodes_df.to_dict('records')
    links_df = pd.read_csv(OUTPUT_FOLDER + links_csv, keep_default_na=False)
    links_df.rename(columns={'from':'source', 'to':'target'}, inplace=True)
    links = links_df.to_dict('records')
    output = {
        'nodes': nodes,
        'links': links
    }
    with open(OUTPUT_FOLDER + output_json, 'w') as f:
        json.dump(output, f, indent=4)






# list_to_csv('enspiral-friends', 'booleanvalue', 'enspiral.csv')
# add_party_to_list('us-congress.csv')
# remove_unpopular_people('enspiral-people.csv', 'enspiral-network.csv', 3)
# populate_profiles('enspiral-people.csv')
# merge_people('enspiral.csv', 'enspiral-people.csv', 'enspiral-people2.csv')
# list_faves_to_csv('enspiral-friends', 'booleanvalue', 'enspiral-faves.csv')
# faves_to_network('enspiral-faves.csv', 'enspiral-network.csv')
# network_to_people('enspiral-network.csv', 'enspiral-people.csv')
# csv_to_gsheet(['us-congress-people-with-party.csv'], '19u2ujgL9PffltGOGnz9lfvi9sKXekkjsvibIuq6PTbg')
# csvs_to_3d_force_graph_json('enspiral-people2.csv', 'enspiral-network.csv', 'enspiral.json')
csvs_to_3d_force_graph_json('us-congress-people-with-party.csv', 'us-congress-network.csv', 'us-congress.json')


# TODO: https://bl.ocks.org/vasturiano/02affe306ce445e423f992faeea13521
# TODO: include even unpopular people
# TODO: Can we get more of long tweets?


# def people_from_network():
#     network = pd.read_csv('network.csv')
#     print('Adding up multiple tweets favorited by & from the same people')
#     network = network.pivot_table(index=['from','to'], values=['text'], aggfunc={'to':'count','text':'last'})
#     network.columns=['last_text','times']
#     network.reset_index(level=['from','to'], inplace=True)
#
#     print('Counting up number of times each person favourited and word frequencies')
#
#     def word_freq(series):
#        combined_text = reduce(lambda x, y: x + ' ' + y, series)
#        freq_table = wordcount(combined_text, 10)
#        return ' '.join(zip(*freq_table)[0])
#
#     people = network.pivot_table(index=['to'], values=['from','last_text'], aggfunc={'from':'count','last_text':word_freq})
#     people.reset_index(level=['to'], inplace=True)
#     people.columns = ['label','favees','liked_tweets_words']
#
#     print('Writing to CSV')
#     people.to_csv('people-in-network.csv', index=False, encoding='utf8')
