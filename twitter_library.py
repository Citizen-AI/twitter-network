# This Python file uses the following encoding: utf-8

import pandas as pd
import json
import requests
import re

import connect_to_twitter
import find_party
import user_faves
from library import print_err, csv_to_gsheet, pd_to_csv


OUTPUT_FOLDER = 'output/'


def list_faves_to_csv(slug, owner_screen_name, out_csv, max_results):
    api = connect_to_twitter.api()
    list_members = api.GetListMembers(slug=slug, owner_screen_name=owner_screen_name)
    for list_member in list_members:
        user_faves.append_to_csv(list_member.screen_name, OUTPUT_FOLDER + out_csv, max_results)


def list_to_csv(slug, owner_screen_name, out_csv):
    print('Saving members of', owner_screen_name, '/', slug)
    api = connect_to_twitter.api()
    list_members = api.GetListMembers(slug=slug, owner_screen_name=owner_screen_name)
    list_members_df = pd.DataFrame()
    for person in list_members:
        data = {'label':person.screen_name, 'name':person.name, 'description':person.description}
        list_members_df = list_members_df.append(data, ignore_index=True)
    pd_to_csv(df=list_members_df, filename=out_csv)


def faves_to_network(faves_csv, network_csv):
    faves = pd.read_csv(OUTPUT_FOLDER + faves_csv)
    print('Adding up multiple tweets favorited by & from the same people')
    network = faves.pivot_table(index=['from','to'], values=['text'], aggfunc={'to':'count','text':'last'})
    network.columns=['last_text','times']
    network.reset_index(level=['from','to'], inplace=True)
    pd_to_csv(df=network, filename=network_csv)


def network_to_people(network_csv, people_csv):
    network = pd.read_csv(OUTPUT_FOLDER + network_csv)
    people = network.pivot_table(index=['to'], aggfunc={'from':'count'})
    people.reset_index(level=['to'], inplace=True)
    people.columns = ['label','favees']
    pd_to_csv(df=people, filename=people_csv)


def remove_unpopular_people(in_people_csv, in_network_csv, out_people_csv, out_network_csv, minimum_favees=1):
    print('Removing people from', in_people_csv, 'and', out_people_csv, 'who have fewer than', minimum_favees, 'connections')
    people = pd.read_csv(OUTPUT_FOLDER + in_people_csv)
    network = pd.read_csv(OUTPUT_FOLDER + in_network_csv)
    popular_people = people.loc[people['favees'] >= minimum_favees]
    network = network.loc[network['to'].isin(popular_people['label'])]
    pd_to_csv(df=popular_people, filename=out_people_csv)
    pd_to_csv(df=network, filename=out_network_csv)

# TODO: append as we go
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


def add_party_to_list(csv, country='us'):
    """Looks for political party affiliation"""
    list_members = pd.read_csv(OUTPUT_FOLDER + csv)
    for index in list_members.index:
        name = list_members.at[index, 'name']
        description = list_members.at[index, 'description']
        party = find_party.search(description, country) or \
                find_party.search(name, country) or \
                find_party.knowledge_graph_get_party(name, country)
        print(name, ',', party)
        if party:
            list_members.at[index, 'party'] = party
    pd_to_csv(df=list_members, filename=csv)


def merge_people(csv1, csv2, output_csv):
    df1 = pd.read_csv(OUTPUT_FOLDER + csv1)
    df2 = pd.read_csv(OUTPUT_FOLDER + csv2)
    merged = pd.merge(df1, df2, how='outer')
    # merged = pd.merge(df1, df2, on=['label','name','description', 'party'], how='outer')
    pd_to_csv(df=merged, filename=output_csv)


def csvs_to_force_graph_json(nodes_csv, links_csv, output_json):
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


def download_images(csv, folder='', column='image', start=0):
    df = pd.read_csv(OUTPUT_FOLDER + csv)
    for url in df[column][start:]:
        try:
            print(url)
            url_stub = re.search(r'(.+)_normal\.(jpe?g|png|gif)', url, re.I)[1]
            filename_stub = re.search(r'.+/(.+)_normal\.(jpe?g|png|gif)', url, re.I)[1]
            filetype = re.search(r'(.+)_normal\.(jpe?g|png|gif)', url, re.I)[2]
            highres_url = url_stub + '_200x200.' + filetype
            filename = filename_stub + '.' + filetype
            r = requests.get(highres_url, allow_redirects=True)
            print('Writing', filename)
            open(OUTPUT_FOLDER + folder + filename, 'wb').write(r.content)
        except:
            print('Skipping', url)
