import os
from pyrxnlp.api.cluster_sentences import ClusterSentences
import pandas as pd
import re

from library import clean_list

# replace this with your api key (see: http://www.rxnlp.com/api-key/)
apikey = "your_api_key"

# Cluster from a list of sentences
# list_of_sentences = [
#     "the sky is so high",
#     "the sky is blue",
#     "fly high into the sky.",
#     "the trees are really tall",
#     "I love the trees",
#     "trees make me happy",
#     "the sun is shining really bright"]

faves = pd.read_csv('output/mps-faves.csv')
tweets = faves['text'].tolist()

for index, tweet in enumerate(tweets):
    tweets[index] = re.sub(r'\bhttp.+?\b|@.+?\b|#.+?\b', '', tweet)

print(tweets[:10])
# print(tweets[:10])
exit()
# initialize sentence clustering
clustering = ClusterSentences ('mnLFXp5MAGmshj2abhyA8qpenoIpp111ieTjsnyCTQZfIxlCsZ')

# generate clusters and print
clusters = clustering.cluster_from_list (list_of_sentences)
if clusters is not None:
    print ("------------------------------")
    print ("Clusters from a list of sentences")
    print ("------------------------------")
    clustering.print_clusters (clusters)
