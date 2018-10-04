# This Python file uses the following encoding: utf-8

import sys

from twitter_library import list_faves_to_csv, list_to_csv, faves_to_network, \
                            network_to_people, remove_unpopular_people, \
                            populate_profiles, add_party_to_list, merge_people, \
                            csvs_to_force_graph_json
from library import csv_to_gsheet


if len(sys.argv) < 2:
    print('Please supply a recipe file with a list of functions to run')
    exit()

recipe_file = sys.argv[1]
with open(recipe_file) as recipe:
    for line in recipe:
        if not line.lstrip().startswith('#'):
            eval(line)


# TODO: Can we get more of long tweets?
# TODO: geolocation on knowledge_graph_get_party?
# TODO: generalise network_to_people
