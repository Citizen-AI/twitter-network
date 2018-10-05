# list_to_csv(owner_screen_name='NZParliament', slug='mps', out_csv='mps.csv')
# add_party_to_list(csv='mps.csv', country='nz')
# list_faves_to_csv(owner_screen_name='NZParliament', slug='mps', out_csv='mps-faves-over-time.csv', max_results=1000)
# faves_to_network('mps-faves.csv', 'mps-network.csv')
# network_to_people(network_csv='mps-faves-over-time.csv', people_csv='mps-people.csv')
# remove_unpopular_people(in_people_csv='mps-people2.csv',
                        # in_network_csv='mps-network.csv',
                        # out_people_csv='mps-people3.csv',
                        # out_network_csv='mps-network3.csv',
                        # minimum_favees=3)
# merge_people(csv1='mps.csv', csv2='mps-people.csv', output_csv='mps-people-plus-mps.csv')
# populate_profiles(people_csv='mps-people-plus-mps.csv')
# csvs_to_force_graph_json(nodes_csv='mps-people-plus-mps.csv', links_csv='mps-faves-over-time.csv', output_json='../graph/mps-over-time.json')
# # csv_to_gsheet(['us-congress-people-with-party.csv'], '19u2ujgL9PffltGOGnz9lfvi9sKXekkjsvibIuq6PTbg')
download_images(csv='mps-people-plus-mps.csv', folder='images/', start=1063)
